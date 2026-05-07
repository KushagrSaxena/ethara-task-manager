from django import forms
from .models import Task, Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }