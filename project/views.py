from typing import Any
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Tasks
from .filters import ProjectFilter
from .forms import ProjectCreateForm, TasksCreateForm

# Create your views here.

def home(request):
    
    return render(request, 'project/home.html')

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/home.html'  # <app>/<model>_<viewtype>.html

    def get_queryset(self):
        # Filter projects based on the logged-in user
        return Project.objects.filter(assigned_users=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProjectFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProjectDetailView(DetailView):
    model = Project
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access assigned_users within get_context_data
        assigned_users = self.object.assigned_users.all()
        context['assigned_users'] = assigned_users

        tasks = self.object.tasks.all()
        context['tasks'] = tasks

        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm

    def form_valid(self, form):
        # Save the project instance first
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()

        # Now that the project has been saved, you can add assigned users
        team = form.cleaned_data['team']
        if team:
            members = team.members.all() 
            for member in members:
                project.assigned_users.add(member)
        
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['name', 'team', 'description', 'start_date', 'due_date', 'status', 'priority']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        project = self.get_object()
        if self.request.user == project.created_by:
            return True
        return False
    
class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = "/"

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.created_by:
            return True
        return False

class TasksCreateView(LoginRequiredMixin, CreateView):
    model = Tasks
    form_class = TasksCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.kwargs['pk']  # Pass the project ID to the form
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['pk'])

       
        return super().form_valid(form)

class TasksUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tasks
    form_class = TasksCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.get_object().project_id 
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        tasks = self.get_object()
        if self.request.user == tasks.created_by:
            return True
        return False
    
class TasksDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tasks

    def test_func(self):
        tasks = self.get_object()
        if self.request.user == tasks.created_by:
            return True
        return False
    
    def get_success_url(self):
        # Redirect to the project detail page after deletion
        task = self.get_object()
        return reverse_lazy('project-detail', kwargs={'pk': task.project.pk})
    
    

class TasksCompleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        task = Tasks.objects.get(pk=self.kwargs['pk'])
        return self.request.user == task.assigned_users.first()

    def post(self, request, *args, **kwargs):
        task = Tasks.objects.get(pk=self.kwargs['pk'])
        task.status = 'completed'
        task.save()
        return HttpResponseRedirect(reverse_lazy('project-detail', kwargs={'pk': task.project.pk}))
