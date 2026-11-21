from django.shortcuts import render
from django.urls import reverse_lazy

from tasks_app.forms import TaskForm
from .models import Task
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
    template_name = 'task_create.html'
    success_url = reverse_lazy('task_list')
    form_class = TaskForm
