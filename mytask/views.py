from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Assignment
from .forms import TaskForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.db.models import Prefetch
from django.contrib import messages
from django.db.models import Q
from django.db.models import OuterRef, Subquery


@login_required
def task_list(request):
    assigned_tasks = Assignment.objects.filter(completed=False).values_list('task_id', flat=True)
    tasks = Task.objects.exclude(id__in=assigned_tasks)
    return render(request, 'task_list.html', {'tasks': tasks})




def deadline_passed(request):
    return render(request, 'deadline_passed.html')

 
@login_required
def return_task(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, student=request.user)

    # Delete the original assignment
    assignment.delete()

    messages.success(request, 'Task returned successfully.')
    return redirect('mytask:task_list')




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mytask:task_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mytask:task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('mytask:login')

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.teacher = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})



def student_task_list(request):
    now = timezone.now()
    assignments = Assignment.objects.filter(student=request.user).select_related('task')
    return render(request, 'student_task_list.html', {'assignments': assignments, 'now': now})


@login_required
def pick_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    assignment = Assignment.objects.create(task=task, student=request.user)
    return redirect('mytask:student_task_list')



def assign_task(request, task_id):
    task = Task.objects.get(id=task_id)
    students = User.objects.filter(is_staff=False)
    if request.method == 'POST':
        student_id = request.POST.get('student')
        assignment = Assignment(task=task, student_id=student_id)
        assignment.save()
        return redirect('task_list')
    return render(request, 'assign_task.html', {'task': task, 'students': students})

def submit_task(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        assignment.completed = True
        assignment.submitted_at = timezone.now()
        assignment.save()
        return redirect('task_list')
    return render(request, 'submit_task.html', {'assignment': assignment})
