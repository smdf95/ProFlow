# Generated by Django 5.0 on 2024-02-09 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_chat_created_by_chat_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(related_name='chat', to='chat.message'),
        ),
    ]
