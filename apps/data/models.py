from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)
    premium = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "Folder", on_delete=models.CASCADE, related_name="owner", blank=True, null=True
    )

    def __str__(self):
        return self.name

    def get_parents(self, id, parents):
        folder = Folder.objects.filter(id=id).first()
        if folder is not None:
            parents.append({"id": folder.id, "name": folder.name})
            if folder.parent:
                return self.get_parents(folder.parent.id, parents)
        return parents

    def sequence(self):
        if not self.parent:
            return [{"id": self.id, "name": self.name}]
        datas = self.get_parents(self.id, [])
        datas.reverse()
        return datas

    def sub_folder(self):
        return Folder.objects.filter(parent=self).count()

    class Meta:
        ordering = ("-id",)


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="media/files")
    permium = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="file")
    size = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
