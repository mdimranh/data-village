from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

STATUS = (("unseen", "Unseen"), ("seen", "Seen"))


class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = PhoneNumberField(region="BD")
    subject = models.TextField()
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default="unseen")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
