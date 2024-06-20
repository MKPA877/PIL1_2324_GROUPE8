import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import PrivateChat, Message
from django.contrib.auth import get_user_model
from django.db import transaction


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'private_chat_{self.chat_id}'

        try:
            self.private_chat = await self.get_private_chat()
        except PrivateChat.DoesNotExist:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'text':
            await self.handle_text_message(data)
        elif message_type in ['image', 'audio', 'video']:
            await self.handle_media_message(data)
        elif message_type == "delete_message":
            await self.handle_delete_message(data)

    async def handle_text_message(self, data):
        message = data['message']
        sender_id = self.scope['user'].id
        new_message = await self.save_message(sender_id, 'text', message)
        await self.send_message_to_group('text', message, sender_id, new_message.id)

    async def handle_text_message(self, data):
        message = data['message']
        sender_id = self.scope['user'].id
        new_message = await self.save_message(sender_id, 'text', message)
        await self.send_message_to_group('text', message, sender_id, new_message.id)


    async def handle_delete_message(self, data):
        message_id = data['message_id']
        await self.delete_message(message_id)
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "delete_message_event",
                "message_id": message_id,
            }
        )

    @sync_to_async
    def get_private_chat(self):
        return PrivateChat.objects.get(id=self.chat_id)

    @sync_to_async
    def save_message(self, sender_id, message_type, content=None):
        # Récupérer l'utilisateur de manière asynchrone
        user = get_user_model().objects.get(pk=sender_id)
        
        # Récupérer la connexion privée pour le message
        private_chat = self.private_chat
        connection = private_chat.connection  # Utilisez la connexion associée à PrivateChat
        
        # Créer un nouveau message avec les données fournies
        with transaction.atomic():
            message_data = {
                'user': user,
                'connection': connection,  # Utilisez l'instance de Connection ici
                message_type: content,
                
            }
            new_message = Message.objects.create(**message_data)
        
        return new_message
    

    @sync_to_async
    def delete_message(self, message_id):
        Message.objects.filter(id=message_id).delete()

    async def send_message_to_group(self, message_type, message, sender_id, message_id):
        message_data = {
            'type': 'chat_message',
            'message_type': message_type,
            'message': message,
            'sender_id': sender_id,
            'message_id': message_id
        }
        await self.channel_layer.group_send(self.room_group_name, message_data)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def delete_message_event(self, event):
        await self.send(text_data=json.dumps(event))
