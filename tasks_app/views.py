from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy

from tasks_app.forms import TaskForm
from .models import Comment, Task
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.select_related(
            'commented_by'
        ).order_by('commented_time')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            Comment.objects.create(
                task=self.object,
                comment=comment_text,
                commented_by=request.user,
            )
        return redirect('task_detail', pk=self.object.pk)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_create.html'
    success_url = reverse_lazy('task_list')
    form_class = TaskForm

    def form_valid(self, form):
        # Set the author to the currently logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_update.html'
    success_url = reverse_lazy('task_list')
    form_class = TaskForm
