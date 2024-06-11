import base64
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from .serializers import UserSerializer


class ChatConsumers(WebsocketConsumer):

    def connect(self):
        user = self.scope['user']
        print(user, user.is_authenticated)
        if not user.is_authenticated:
            return
        #Save username to use as a group name for this user
        self.username = user.username
        #Join this user to a group with their username
        async_to_sync(self.channel_layer.group_add)(
            self.username, self.channel_name
        ) 
        self.accept()
    
    def disconnect(self, close_code):
        #Leave room/group
        async_to_sync(self.channel_layer.group_discard)(
            self.username, self.channel_name
        ) 

    #------------------------
    #     Handle requests
    #------------------------

    def receive(self, text_data):
        # Receive message from websocket
        data = json.loads(text_data)
        data_source = data.get('source')

        #Pretty print python dict
        print('receive', json.dumps(data, indent=2))

        #Thumbnail upload 
        if data_source == 'thumbnail':
            self.receive_thumbnail(data)

    
    def receive_thumbnail(self, data):
        user = self.scope['user']
        # Convert base64 data to django content file
        image_str = data.get('base64')
        image = ContentFile(base64.b64deco(image_str))
        # Update thumbnail.field
        filename = data.get('filename')
        user.thumbnail.save(filename, image, save=True)
        #Serialize user
        serialized = UserSerializer(user)
        # Send updated user data including new thumbnail
        self.send_group(self.username, 'thumbnail', serialized.data)



    #--------------------------------------------
    #   Catch/all broadcast to client helpers
    #--------------------------------------------

    def send_group(self, group, source, data):
        response = {
            'type': 'broadcast_group',
            'source': source,
            'data': data
        }
        async_to_sync(self.channel_layer.group_send)(
            group, response
        ) 
    
    def broadcast(self, data):
        '''
        data
            - type: 'broadcast_group'
            - source: where it originated from
            - data: what ever you want to send as a dict
        '''
        data.pop('type')
        '''
        return data
            - source: where it originated from
            - data: what ever you want to send as a dict
        '''
        self.send(text_data=json.dumps(data))