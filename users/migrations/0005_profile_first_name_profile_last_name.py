# Generated by Django 5.0 on 2024-02-06 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
