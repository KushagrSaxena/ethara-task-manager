from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_projects'
    )

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assigned_tasks'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField()

    def __str__(self):
        return self.title