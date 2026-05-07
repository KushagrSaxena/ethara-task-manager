from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('project/create/', views.create_project, name='create-project'),
    path('task/create/', views.create_task, name='create-task'),
    path('task/<int:pk>/update/', views.update_task_status, name='update-task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete-task'),
]
