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
from .forms import ProjectCreateForm

# Create your views here.
def home(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'project/home.html', context)

class ProjectListView(ListView):
    model = Project
    template_name = 'project/home.html'  # <app>/<model>_<viewtype>.html


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

        task_users = self.object.tasks.values_list('assigned_users', flat=True).distinct()
        task_users = self.request.user.__class__.objects.filter(pk__in=task_users)
        context['task_users'] = task_users

        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['name', 'description', 'start_date', 'due_date', 'status', 'priority', 'assigned_users']

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
    fields = ['name', 'description', 'status', 'start_date', 'due_date', 'assigned_users']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

class TasksUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tasks
    fields = ['name', 'description', 'status', 'start_date', 'due_date', 'assigned_users']

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
