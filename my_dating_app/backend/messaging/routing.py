"""Ici il faut définir les routes WebSockets de l'application
"""
from django.urls import path, re_path # Importer la fonction 'path' pour définir les routes WebSockets
from ..messaging import consumers   # Importer le module où le consommateur WebSocket (ChatConsumer) est défini

websocket_urlpatterns = [   # Liste des routes WebSocket. Chaque entrée dans cette liste mappe une URL à un consommateur.
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),  # Cette ligne définit une route WebSocket
    re_path(r'ws/chat/(?P<sender_id>\d+)/(?P<recipient_id>\d+)/$', consumers.ChatConsumer.as_asgi())]