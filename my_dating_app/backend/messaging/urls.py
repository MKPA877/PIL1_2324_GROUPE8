from django.urls import path
from . import consumers
from .views import ConversationListView, ConversationCreateView, ConversationDetailView, MessageCreateView

websocket_urlpatterns = [
    path('ws://example.com/ws/chat/', consumers.ChatConsumer.as_asgi()),

]

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversation_list'),
    path('conversations/new/', ConversationCreateView.as_view(), name='conversation_create'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversations/<int:pk>/messages/new/', MessageCreateView.as_view(), name='message_create'),
]