from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView, 
    ProjectCreateView, 
    ProjectUpdateView, 
    ProjectDeleteView,
    TasksCreateView,
    TasksDeleteView,
    TasksUpdateView,
    TasksCompleteView,
)
from . import views

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-home'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('project/new', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete', ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<int:pk>/tasks/new', TasksCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>', TasksUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TasksDeleteView.as_view(), name='task-delete'),
    path('complete-task/<int:pk>/', TasksCompleteView.as_view(), name='task-complete'),
]