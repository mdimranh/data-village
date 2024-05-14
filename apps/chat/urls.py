from django.urls import path

from .views import ChatView, Messages, MyRooms, room

urlpatterns = [
    path("chat/<str:rid>", ChatView),
    path("chat", ChatView),
    path("rooms/<str:roomid>", MyRooms),
    path("messages/<int:uid>", Messages),
    path("room/<str:slug>/", room, name="chat"),
]
