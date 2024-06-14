import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PrivateChat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        user = self.scope['user']

        # Vérifier l'authentification de l'utilisateur et s'il est autorisé à accéder à cette discussion
        if not user.is_authenticated:
            await self.close()
            return

        try:
            chat = PrivateChat.objects.get(id=self.chat_id)
            if user != chat.user1 and user != chat.user2:
                await self.close()
                return
        except PrivateChat.DoesNotExist:
            await self.close()

        self.room_group_name = f'private_chat_{self.chat_id}'
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

    async def handle_text_message(self, data):
        message = data['message']
        sender_id = self.scope['user'].id
        await self.save_message(sender_id, 'text', message)
        await self.send_message('text', message, sender_id)

    async def handle_media_message(self, data):
        message_type = data['type']
        message = data['message']
        sender_id = self.scope['user'].id
        await self.save_message(sender_id, message_type)
        await self.send_message(message_type, message, sender_id)

    async def save_message(self, sender_id, message_type, content=None):
        try:
            message = Message.objects.create(user_id=sender_id, **{message_type: content})
            return message
        except Exception as e:
            print(f"Error saving message: {e}")
            return None

    async def send_message(self, message_type, message, sender_id):
        message_data = {'message_type': message_type, 'message': message, 'sender_id': sender_id}
        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat.message', **message_data})

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        await self.send(text_data=json.dumps({'message': message, 'sender_id': sender_id}))
