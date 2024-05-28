from django.views.generic import ListView, CreateView, DetailView
from .models import Conversation, Message
from .forms import ConversationForm, MessageForm

class ConversationListView(ListView):
    model = Conversation
    template_name = 'messaging/conversation_list.html'

class ConversationCreateView(CreateView):
    model = Conversation
    form_class = ConversationForm
    template_name = 'messaging/conversation_form.html'
    success_url = '/conversations/'

class ConversationDetailView(DetailView):
    model = Conversation
    template_name = 'messaging/conversation_detail.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messaging/message_form.html'

    def form_valid(self, form):
        form.instance.conversation = Conversation.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)