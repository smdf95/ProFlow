# Generated by Django 5.0 on 2024-02-01 14:15

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, default='default.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 300], upload_to='profile_pics'),
        ),
    ]
