# Generated by Django 5.0 on 2024-02-10 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_tasks_status'),
        ('teams', '0007_remove_teams_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='teams.teams'),
            preserve_default=False,
        ),
    ]
