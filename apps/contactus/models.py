from django.db import models

STATUS = (("unseen", "Unseen"), ("seen", "Seen"))


class Message(models.Model):
    email = models.EmailField()
    subject = models.TextField()
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default="unseen")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
