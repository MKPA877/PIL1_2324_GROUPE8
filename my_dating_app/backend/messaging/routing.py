from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sender_id>\d+)/(?P<recipient_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
