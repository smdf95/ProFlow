from django import forms
from django.contrib.auth.models import User
from project.models import Project, Tasks
from teams.models import Teams


class ProjectCreateForm(forms.ModelForm):

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter users based on the user's team membership
            self.fields['teams'].queryset = Teams.objects.filter(teams__members=user)

    class Meta:
        model = Project
        fields = ['name', 'team', 'description', 'start_date', 'due_date', 'status', 'priority']


class TasksCreateForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'start_date', 'due_date', 'assigned_users']

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        if project_id:
            project = Project.objects.get(id=project_id)
            self.fields['assigned_users'].queryset = project.team.members.all()





