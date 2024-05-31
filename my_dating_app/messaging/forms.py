from django import forms
from .models import Conversation, Message

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'conversation']

