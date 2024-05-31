from django.urls import path
from .views import ConversationListView, ConversationCreateView, ConversationDetailView, MessageCreateView
from . import views

urlpatterns = [
    path('conversations/', views.conversation_list, name='conversation_list'),  # Page pour voir la liste des conversations
    path('chat/<int:conversation_id>/', views.chat_room, name='chat_room'),  # Page de chat entre deux utilisateurs
    path('send_message/<int:conversation_id>/', views.send_message, name='send_message'),  # Envoi de message
    path('start_conversation/<int:user_id>/', views.start_new_conversation, name='start_conversation'),  # Commencer une nouvelle conversation
    #path('delete_conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),  #Supprimer une conversation
    #path('block_user/<int:user_id>/', views.block_user, name='block_user'),   # Bloquer un utilisateur 
]

