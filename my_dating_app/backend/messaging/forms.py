from django import forms
from .models import Conversation, Message

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['participants']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content']

