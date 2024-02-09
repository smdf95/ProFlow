from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image, ExifTags
from project.models import Project


class Teams(models.Model):

    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_leader')
    projects = models.ManyToManyField(Project, blank=True, related_name='teams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams_created')

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('team-detail', kwargs={'pk': self.pk})