# Generated by Django 5.0 on 2024-02-08 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_tasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], max_length=11),
        ),
    ]