import uuid

from django.db import connection, models
from django.db.models import Max, OuterRef, Subquery
from django.shortcuts import render

from account.models import User

from .models import Chat, Room


def ChatView(request, uid):
    other_user = User.objects.get(id=uid)
    current_user = request.user
    room = Room.objects.filter(participants=current_user).filter(participants=other_user).first()
    if room is None:
        room = Room.objects.create()
        room.participants.add(current_user)
        room.participants.add(other_user)

    # Subquery to get the most recent message for each room
    last_message_subquery = Chat.objects.filter(room=OuterRef('pk')).order_by('-created_at').values("body", "sender__email", "sender__phone", "sender__id")[:1]

    messages = Chat.objects.filter(room__id=room.id).order_by('-created_at')

    context = {
        "roomid": room.roomid,
        "partner": other_user,
        "messages": messages
    }
    return render(request, 'chat/chat.html', context)

def MyRooms(request, roomid):
    # Subquery to get the most recent message for each room
    last_message_subquery = Chat.objects.filter(room=OuterRef('pk')).order_by('-created_at').values("body", "sender__email", "sender__phone", "sender__id")[:1]

    # Query to retrieve all rooms with the most recent message
    rooms = Room.objects.filter(participants=request.user).order_by('-last_updated')
    results = []
    for r in rooms:
        r.partner = r.participants.all().exclude(id = request.user.id).first()
        r.message = Chat.objects.filter(room__id=r.id).order_by('-created_at').first()
        if r.message is not None:
            results.append(r)
    context = {
        "roomid": roomid,
        "rooms": results
    }
    return render(request, 'chat/rooms.html', context)

def Messages(request, uid):
    user = User.objects.get(id=uid)
    room = Room.objects.filter(participants=request.user).filter(participants=user).first()
    if room is None:
        room = Room.objects.create()
        room.participants.add(request.user)
        room.participants.add(user)
    messages = Chat.objects.filter(room__id=room.id).order_by('-created_at')[:30]
    context = {
        "roomid": room.roomid,
        "messages": messages,
        "partner": user
    }
    return render(request, 'users/messages.html', context)

def room(request, slug):
    return render(request, 'chat/room.html', {'name': "test", 'slug': "abc"})
