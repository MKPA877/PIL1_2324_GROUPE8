"""
ASGI config for my_dating_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
"""Ici il faut configurer 
les protocoles que l'application Django doit gérer, notamment les requêtes HTTP et les connexions WebSocket.
"""
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import messaging.routing

# Définir les paramètres de l'application Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_dating_app.settings')

# Initialiser Django
django.setup()

# Définir l'application ASGI
application = ProtocolTypeRouter({
    # Gérer les requêtes HTTP avec l'application ASGI de Django
    'http': get_asgi_application(),

    # Gérer les connexions WebSocket
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                messaging.routing.websocket_urlpatterns  # Définir les URL WebSocket dans le module de routage
            )
        )
    ),
})

