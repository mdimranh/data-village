import uuid

from django.db import models
from django_jsonform.models.fields import ArrayField

from account.models import User


def roomid_generate():
    rid = uuid.uuid4().hex[:20]
    return rid

class Room(models.Model):
    roomid = models.CharField(default=roomid_generate, editable=False, unique=True, max_length=30)
    participants = models.ManyToManyField(User)
    name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

STATUS = (
    ("sent", "Sent"),
    ("delivered ", "Delivered "),
    ("seen", "Seen")
)

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sender")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room")
    body = models.TextField()
    images = ArrayField(models.ImageField(upload_to="chat/image"), size=10, blank=True, null=True)
    files = ArrayField(models.FileField(upload_to="chat/file"), size=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, default="sent")

    def __str__(self):
        return self.body[:50]+"..." if len(self.body) > 50 else self.body
