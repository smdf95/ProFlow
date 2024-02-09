from django.urls import path
from .views import ChatsList, ChatCreateView, ChatUpdateView, ChatDeleteView, ChatMessages
from . import views

urlpatterns = [
    path('', ChatsList.as_view(), name='chat-list'),
    path('<int:pk>', ChatMessages, name='chat-detail'),
    path('new', ChatCreateView.as_view(), name='chat-create'),
    path('<int:pk>/update', ChatUpdateView.as_view(), name='chat-update'),
    path('<int:pk>/delete', ChatDeleteView.as_view(), name='chat-delete'),
]