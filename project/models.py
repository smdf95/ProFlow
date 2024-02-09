from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

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

    def get_absolute_url(self): # Change here
        return reverse('project-detail', kwargs={'pk': self.pk}) # Change here to bring the user to the post detail view
    
class Tasks(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=11, choices=[('active', 'Active'), ('completed', 'Completed')])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_users = models.ManyToManyField('auth.User', related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self): # Change here
        return reverse('project-detail', kwargs={'pk': self.project.pk}) # Change here to bring the user to the post detail view

