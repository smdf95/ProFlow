from typing import Any
from django.forms import MultipleChoiceField, CheckboxSelectMultiple
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.base import View
from django.utils import timezone
from django.utils.timesince import timesince
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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

class TeamsListView(LoginRequiredMixin, ListView):
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

        usernames = [user.username for user in member_usernames]

        # Retrieve the corresponding User objects
        users = User.objects.filter(username__in=usernames)

        # Set the created_by and team_leader fields
        form.instance.created_by = self.request.user
        team = form.save(commit=False)
        
        # Set the team leader as the current user
        team.team_leader = self.request.user
        
        # Save the team instance to get a primary key (ID)
        team.save()
        
        # Add each user to the team's members
        for user in users:
            send_invitation_email(team, user.email, self.request)

        # Set the many-to-many relationship with the members field

        return super().form_valid(form)
    

def send_invitation_email(team, email, request):

    token = default_token_generator.make_token(team.team_leader)
    
    # Encode the team ID and token
    team_id_b64 = urlsafe_base64_encode(str(team.id).encode())
    token_b64 = urlsafe_base64_encode(token.encode())
    invitation_link = request.build_absolute_uri(reverse('accept-invitation')) + f'?team_id={team_id_b64}&token={token_b64}'
    host_email = settings.EMAIL_HOST_USER
    send_mail(
        'Invitation to join team',
        f'You have been invited to join the team "{team.name}". Click the link to accept: {invitation_link}. If you do not wish to join {team.name}, please ignore the email.',
        host_email,
        [email],
        fail_silently=False,
    )


def accept_invitation(request):
    if request.method == 'GET':
        # Retrieve the team ID and token from the request
        team_id_b64 = request.GET.get('team_id')
        token_b64 = request.GET.get('token')
        
        # Decode the team ID and token
        try:
            team_id = urlsafe_base64_decode(team_id_b64).decode()
            token = urlsafe_base64_decode(token_b64).decode()
        except (TypeError, ValueError, OverflowError):
            # Handle invalid data (e.g., invalid base64 encoding)
            return HttpResponse('Invalid invitation link')
        
        # Retrieve the team instance
        team = get_object_or_404(Teams, pk=team_id)
        
        # Verify the token
        if default_token_generator.check_token(team.team_leader, token):
            # Add the current user to the team's members
            team.members.add(request.user)
            
            # Optionally, you can perform additional actions here
            
            # Redirect to a success page
            return render(request, 'teams/accept_invite.html')
        else:
            # Handle invalid token
            return HttpResponse('Invalid invitation link')
    else:
        # Handle unsupported HTTP methods
        return HttpResponse('Method not allowed')

