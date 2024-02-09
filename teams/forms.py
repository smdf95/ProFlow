from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Teams

class TeamForm(forms.ModelForm):

    member_usernames = forms.CharField(label="Member Usernames", max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Create'))

    def clean_member_usernames(self):
        member_usernames = self.cleaned_data.get('member_usernames')
        # Split the input string into a list of usernames
        usernames = [username.strip() for username in member_usernames.split(',') if username.strip()]
        # Filter existing users by usernames
        users = User.objects.filter(username__in=usernames)
        if len(usernames) != len(users):
            raise forms.ValidationError("One or more usernames are invalid.")
        return users
    
    class Meta:
        model = Teams
        fields = ['name', 'member_usernames']





