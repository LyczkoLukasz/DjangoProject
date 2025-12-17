import json
from channels.generic.websocket import AsyncWebsocketConsumer
#from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        # Każdy użytkownik ma swoją unikalną grupę WebSocket
        self.group_name = f'notifications_{self.scope["user"].id}'

        # Dołączenie do grupy
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Opuszczenie grupy
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        notification = event['notification']

        # Wyślij wiadomość przez WebSocket
        await self.send(text_data=json.dumps({
            'notification': notification
        }))

