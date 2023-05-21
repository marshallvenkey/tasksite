from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'mytask'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:task_id>/pick/', views.pick_task, name='pick_task'),
    path('student/tasks/', views.student_task_list, name='student_task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/assign/', views.assign_task, name='assign_task'),
    path('assignments/<int:assignment_id>/submit/', views.submit_task, name='submit_task'),
    path('return-task/<str:assignment_id>/', views.return_task, name='return_task'),
    path('deadline-passed/', views.deadline_passed, name='deadline_passed'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
