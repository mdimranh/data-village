import json

# from api.utils import CustomSerializer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone

from account.models import User

from .models import Chat, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        roomid = self.scope["url_route"]["kwargs"]["roomid"]
        self.room_name = roomid
        self.user = self.scope["user"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # await self.send(text_data=self.room_group_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.send(text_data=self.room_group_name)
        body = data["message"]

        await self.save_message(
            sender=self.scope["user"].id, body=data["message"], room=self.room_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": body, "sender": self.scope["user"].id},
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        message_html = f"<div hx-swap-oob='beforeend:#newmessages'><div class='x{sender}-message'><p class='px-4 py-2 rounded-3xl max-w-2xl w-fit bg-gray-200 rounded-bl-none'>{message}</p></div></div>"
        await self.send(
            text_data=json.dumps({"message": message_html, "sender": sender})
        )

    @database_sync_to_async
    def save_message(self, sender, body, room):
        _sender = User.objects.get(id=sender)
        _room = Room.objects.get(roomid=room)
        Chat.objects.create(sender=_sender, body=body, room=_room)
        _room.last_updated = timezone.now()
        _room.save()


class ChatConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_slug"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.user
        username = "test"
        room = self.room_name

        # await self.save_message(room, user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                # "room": room,
                "username": username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        # room = event["room"]
        username = event["username"]

        message_html = f"<div hx-swap-oob='beforeend:#messages'><p><b>{username}</b>: {message}</p></div>"
        await self.send(
            text_data=json.dumps(
                {
                    "message": message_html,
                    # "room": room,
                    "username": username,
                }
            )
        )


class ConnectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["id"]
        self.room_group_name = "connect_%s" % self.room_name
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.change_status(True)

    @database_sync_to_async
    def change_status(self, online=False):
        self.user.online = online
        self.user.save()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.change_status(False)
