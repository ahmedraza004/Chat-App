# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called when WebSocket connects
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Called when WebSocket disconnects
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Called when a message is received from WebSocket
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']

        # Save message to DB
        sender = await database_sync_to_async(User.objects.get)(username=sender_username)
        msg = await database_sync_to_async(Message.objects.create)(
            sender=sender, room_name=self.room_name, content=message
        )

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'timestamp': str(msg.timestamp)
            }
        )

    async def chat_message(self, event):
        # Called when group sends a message
        await self.send(text_data=json.dumps(event))

    