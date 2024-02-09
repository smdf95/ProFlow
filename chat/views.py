from typing import Any
from django.forms import MultipleChoiceField, CheckboxSelectMultiple
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.utils import timezone
from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Chat, ChatMessage
from .forms import ChatCreateForm, MessageForm


# Create your views here.
@login_required
def home(request):
    

    context = {
        'chats': Chat.objects.all(),
    }
    return render(request, 'chat/chats_list.html', context)

class ChatsList(ListView):
    model = Chat
    template_name = 'chat/chats_list.html'
    context_object_name = 'chats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chats = context['chats']

        current_time = timezone.now()

        for chat in chats:
            if chat.last_updated:
                time_diff = current_time - chat.last_updated
                if time_diff.total_seconds() <= 24*3600:
                    chat.time_diff = timesince(chat.last_updated)
                else:
                    chat.time_diff = None
            else:
                chat.time_diff = None

        return context
    

# class ChatDetail(DetailView):
#     model = Chat

def ChatMessages(request, pk):
    chat = Chat.objects.get(id=pk)
    chat_messages = chat.messages.all()


    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.save()
            chat.messages.add(new_message)
            chat.last_updated = timezone.now()
            chat.save(update_fields=['last_updated'])
            return redirect('chat-detail', pk=chat.pk)
    
    else:
        form = MessageForm()



    context = {
        'chat': chat,
        'chat_messages': chat_messages,
        'form': form,      # Pass the MessageForm
    }

    return render(request, 'chat/chat_detail.html', context)



class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = ChatCreateForm
    template_name = 'chat/chat_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class ChatUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chat
    form_class = ChatCreateForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        chat = self.get_object()
        if self.request.user == chat.created_by:
            return True
        return False
    
class ChatDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chat
    success_url = "/"

    def test_func(self):
        chat = self.get_object()
        if self.request.user == chat.created_by:
            return True
        return False



