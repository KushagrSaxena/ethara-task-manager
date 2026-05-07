from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views  # Import your custom user views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # User Registration
    path('register/', user_views.register, name='register'),
    
    # Built-in Django auth for Login/Logout
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Task Manager Logic (Project & Task URLs)
    path('', include('tasks.urls')),
]