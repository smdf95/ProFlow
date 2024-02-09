from typing import Any
from django.forms import MultipleChoiceField, CheckboxSelectMultiple
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.utils import timezone
from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Teams
from .forms import TeamForm

def home(request):
    if request.user.is_authenticated:
        return redirect('teams-list')
    else:
        return render(request, 'project/home.html')

class TeamsListView(ListView):
    model = Teams
    template_name = 'teams_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_teams = Teams.objects.filter(members=self.request.user)
        context['user_teams'] = user_teams
        return context
    
class TeamDetailView(DetailView):
    model = Teams



class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Teams
    form_class = TeamForm
    template_name = 'teams/teams_form.html'

    
    def form_valid(self, form):
        # Retrieve the usernames from the form
        member_usernames = form.cleaned_data.get('member_usernames', [])

        # Retrieve the corresponding User objects
        users = User.objects.filter(username__in=member_usernames)

        # Set the created_by and team_leader fields
        form.instance.created_by = self.request.user
        form.instance.team_leader = self.request.user

        # Save the Team instance to the database
        form.instance.save()

        # Set the many-to-many relationship with the members field
        form.instance.members.set(users)

        return super().form_valid(form)
    

