import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, ChatRoom, Influencer, Sponsor
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to database
        room = await sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        influencer = await sync_to_async(Influencer.objects.get)(user_id=self.scope['user'])
        sponsor = await sync_to_async(Sponsor.objects.get)(user_id=self.scope['user'])

        await sync_to_async(Chat.objects.create)(
            room=room,
            influencer_id=influencer,
            sponser_id=sponsor,
            content=message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
