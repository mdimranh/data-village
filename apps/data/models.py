from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)
    premium = models.BooleanField(default=False)
    color = models.CharField(max_length=255, default="#4B5563")
    parent = models.ForeignKey("Folder", on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return self.name
    
