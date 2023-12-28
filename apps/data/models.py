from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)
    premium = models.BooleanField(default=False)
    color = models.CharField(max_length=255, default="#4B5563")
    parent = models.ForeignKey("Folder", on_delete=models.CASCADE, related_name="owner", blank=True, null=True)

    def __str__(self):
        return self.name

    def sub_folder(self):
        return Folder.objects.filter(parent=self).count()

    class Meta:
        ordering = ('-id',)
    
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="media/files")
    permium = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="file")
    size = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)