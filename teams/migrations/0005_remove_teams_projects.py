# Generated by Django 5.0 on 2024-02-09 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_teams_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='projects',
        ),
    ]