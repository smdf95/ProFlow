from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Chat, ChatMessage

class ChatCreateForm(forms.ModelForm):
    # Fetch a queryset of users
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        print(user)
        if user:
            # Filter users based on the user's team membership
            self.fields['users'].queryset = User.objects.filter(teams__members=user).distinct()
    class Meta:
        model = Chat
        fields = ['name', 'users', 'image']


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Send'))
        
        # Add form-control class to content field
        self.fields['content'].widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'cols': 40}),
        }

    # No changes to your existing code, just add this:
