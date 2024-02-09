from django.urls import path
from .views import TeamsListView, TeamCreateView, TeamDetailView
from . import views

urlpatterns = [
    path('', TeamsListView.as_view(), name='teams-list'),
    path('<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('create/', TeamCreateView.as_view(), name='team-create'),
]