from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
import json
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
import logging
from .models import Message, Conversation
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):  
        # Gérer la connexion du client
        
        # Récupérer les IDs de l'expéditeur et du destinataire de l'URL
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        # Générer le nom de la salle de discussion en fonction des IDs de l'expéditeur et du destinataire
        self.room_name = f'chat_{self.sender_id}_{self.recipient_id}'

        # Ajouter le client au groupe de canaux de la discussion privée
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        # Accepter la connexion WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Gérer la déconnexion du client
        
        # Retirer le client du groupe de canaux de la discussion privée
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

        # Envoyer un message de déconnexion à tous les autres participants
        await self.channel_layer.group_send(
            'discussion',  # Nom du groupe de canaux de la discussion
            {
                'type': 'user.disconnected',
                'channel_name': self.channel_name
            }
        )

    async def user_disconnected(self, event):
        # Gérer l'événement de déconnexion d'un utilisateur
        
        # Récupérer le nom du canal du client déconnecté à partir de l'événement
        channel_name = event['channel_name']
        
        # Envoyer un message informant de la déconnexion
        await self.send(text_data=json.dumps({
            'type': 'user.disconnected',
            'channel_name': channel_name
        }))

    async def receive(self, text_data):
        # Gérer la réception d'un nouveau message
        
        # Analyser le message reçu
        data = json.loads(text_data)
        message_content = data['message']
        sender = self.scope['user']

        # Récupérer l'ID du destinataire et l'objet correspondant à partir des données reçues
        recipient_id = data['recipient_id']
        recipient = await sync_to_async(User.objects.get)(id=recipient_id)

        # Récupérer l'ID de la conversation et l'objet correspondant à partir des données reçues
        conversation_id = data['conversation_id']
        conversation = await sync_to_async(Conversation.objects.get)(id=conversation_id)

        # Créer un nouveau message et l'enregistrer dans la base de données
        new_message = await sync_to_async(Message.objects.create)(
            sender=sender,
            recipient=recipient,
            content=message_content,
            conversation=conversation
        )

        # Envoyer le message au groupe de la discussion
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'content': message_content,
                'sender': sender.username,
                'recipient': recipient.username,
                'timestamp': str(datetime.now()),
            }
        )

    async def chat_message(self, event):
        # Gérer l'envoi d'un message de chat à tous les participants de la discussion
        
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': event['content'],
            'sender': event['sender'],
            'recipient': event['recipient'],
            'timestamp': event['timestamp'],
        }))

    async def send_message_to_recipient(self, content, sender, recipient):
        # Envoyer un message privé à un utilisateur spécifié
        
        message = {
            'type': 'chat_message',
            'content': content,
            'sender': sender.username,
            'recipient': recipient.username,
            'timestamp': str(datetime.now()),
        }

        try:
            # Envoyer le message au groupe de discussion correspondant
            await self.channel_layer.group_send(
                self.room_name,
                message
            )
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi du message au destinataire {recipient.username}: {e}")
