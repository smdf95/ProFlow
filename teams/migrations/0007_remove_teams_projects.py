# Generated by Django 5.0 on 2024-02-10 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_teams_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='projects',
        ),
    ]
