from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
