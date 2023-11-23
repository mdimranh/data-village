from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<str:roomid>", consumers.ChatConsumer.as_asgi()),
    path('chat/<str:room_slug>/', consumers.ChatConsumers.as_asgi()),
]