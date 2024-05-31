from django.test import TestCase

# Create your tests here.
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.test import TestCase
from  .consumers import ChatConsumer
import json
import pytest

@pytest.mark.asyncio
async def test_chat_consumer():
    communicator = WebsocketCommunicator(ChatConsumer, "/ws/chat/sender_id/recipient_id/")
    connected, _ = await communicator.connect()

    # Vérifie la connexion
    assert connected

    # Vérifie que le groupe a été ajouté
    channel_layer = get_channel_layer()
    groups = await channel_layer.group_channels("chat_sender_id_recipient_id")
    assert communicator.channel_name in groups

    # Envoie un message
    message = {
        "message": "Test message",
        "recipient_id": 2,
        "conversation_id": 1
    }
    await communicator.send_json_to(message)

    # Vérifie la réception du message
    response = await communicator.receive_json_from()
    assert response["message"] == "Test message"

    # Déconnexion
    await communicator.disconnect()
