from django.db import models

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('Essential', 'Essential'),
        ('Basicly on nearest time', 'Basicly on nearest time'),
        ('Long_dated', 'Long_dated'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    started_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=25, choices=PRIORITY_CHOICES)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField()
    commented_time = models.DateTimeField(auto_now_add=True)
    # Older comments may have a free-text author that cannot be matched to a user.
    commented_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Comment for task: {self.task.title} at {self.commented_time}"
