# chat/consumers.py
import json

from chat_backend.models import Message, ChatRoom
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.signals import post_save
from chat_backend.serializers import MessageSerializer

from channels.db import database_sync_to_async
from django.dispatch import receiver


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, msg):
        return Message.objects.create(text=msg, room=self.room)

    @database_sync_to_async
    def get_messages(self):
        self.room, created = ChatRoom.objects.get_or_create(name=self.room_name)
        messages = list(Message.objects.filter(room=self.room))
        print("all messages", messages)
        return messages

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        messages = await self.get_messages()
        print("all messages", messages)
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        for message in messages:
            #message_json = MessageSerializer(message).data
            await self.send(text_data=json.dumps({"message": message.text, "id": message.id}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        new_msg = await self.create_chat(message) 
        print("recieve_message", message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": new_msg.text, "id": new_msg.id}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        id = event["id"]
        print("send_message", message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "id": id,}))
