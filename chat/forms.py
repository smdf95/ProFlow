from django import forms
from django.contrib.auth.models import User
from .models import Chat, ChatMessage

class ChatCreateForm(forms.ModelForm):
    # Fetch a queryset of users
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Chat
        fields = ['name', 'users', 'image']

class MessageForm(forms.ModelForm):

    class Meta:
        model = ChatMessage
        fields = ['content']
