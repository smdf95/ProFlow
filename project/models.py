from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=9, choices=[('active', 'Active'), ('completed', 'Completed'), ('inactive', 'Inactive')])
    priority = models.CharField(max_length=6, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    assigned_users = models.ManyToManyField('auth.User', related_name='assigned_projects')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

