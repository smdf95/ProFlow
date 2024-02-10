# Generated by Django 5.0 on 2024-02-10 18:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_remove_project_assigned_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='assigned_users',
            field=models.ManyToManyField(related_name='assigned_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
