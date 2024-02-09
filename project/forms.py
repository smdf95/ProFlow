from django import forms
from django.contrib.auth.models import User
from .models import Project

class ProjectCreateForm(forms.ModelForm):

    assigned_users = forms.ModelMultipleChoiceField(
                        queryset=User.objects.all(),
                        widget=forms.CheckboxSelectMultiple
                )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'due_date', 'status', 'priority', 'assigned_users']





