from django.shortcuts import render
from django.views.generic import ListView

from apps.contactus.models import Message


class MessageListView(ListView):
    model = Message
    template_name = "dashboard/message/messages.html"

    def get_queryset(self):
        return Message.objects.all()
