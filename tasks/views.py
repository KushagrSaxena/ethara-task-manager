from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib import messages
from .models import Project, Task
from .forms import ProjectForm, TaskForm

@login_required
def dashboard(request):
    user = request.user
    
    if user.role == 'admin':
        projects = Project.objects.all()
        # Tasks assigned specifically to the logged-in Admin
        my_tasks = Task.objects.filter(assigned_to=user).order_by('due_date')
        # Tasks assigned to all other employees
        employee_tasks = Task.objects.exclude(assigned_to=user).order_by('due_date')
    else:
        # Members only see their own tasks
        my_tasks = Task.objects.filter(assigned_to=user).order_by('due_date')
        employee_tasks = None
        projects = Project.objects.filter(tasks__assigned_to=user).distinct()

    context = {
        'projects': projects,
        'my_tasks': my_tasks,
        'employee_tasks': employee_tasks,
        'is_admin': user.role == 'admin',
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def create_project(request):
    """
    Allows Admins to create new projects.
    """
    if request.user.role != 'admin':
        raise PermissionDenied

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    
    return render(request, 'tasks/project_form.html', {'form': form})

@login_required
def create_task(request):
    """
    Allows Admins to create and assign tasks.
    """
    if request.user.role != 'admin':
        raise PermissionDenied

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully!")
            return redirect('dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def update_task_status(request, pk):
    """
    Updates task status. Supports HTMX for partial page updates.
    """
    task = get_object_or_404(Task, pk=pk)
    
    # Permission Check: Only the assignee or an admin can update status
    if request.user == task.assigned_to or request.user.role == 'admin':
        if request.method == "POST":
            new_status = request.POST.get('status')
            
            # Use the model's choices for validation
            valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
            if new_status in valid_statuses:
                task.status = new_status
                task.save()
            
            # HTMX Logic: return only the task snippet
            if hasattr(request, 'htmx') and request.htmx:
                return render(request, 'tasks/partials/task_row.html', {'task': task})
            
            return redirect('dashboard')
    else:
        raise PermissionDenied

@login_required
def delete_task(request, pk):
    """
    Strictly Admin-only task deletion.
    """
    if request.user.role != 'admin':
        raise PermissionDenied
    
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    
    if hasattr(request, 'htmx') and request.htmx:
        # Return empty response so HTMX removes the element from the DOM
        return HttpResponse("") 
        
    return redirect('dashboard')