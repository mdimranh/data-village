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

    def total_file(self):
        return FilePackage.objects.filter(folder=self).count()

    class Meta:
        ordering = ("-id",)


class FilePackage(models.Model):
    name = models.CharField(max_length=255)
    premium = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="folder")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)

    def files(self):
        return File.objects.filter(package__id=self.id)

    def pdf(self):
        return File.objects.filter(package__id=self.id, type=".pdf").first()

    def xlsx(self):
        return File.objects.filter(package__id=self.id, type=".xlsx").first()

    def xls(self):
        return File.objects.filter(package__id=self.id, type=".xls").first()

    def ppt(self):
        ppt = File.objects.filter(package__id=self.id, type=".ppt").first()
        if ppt:
            return ppt
        pptx = File.objects.filter(package__id=self.id, type=".pptx").first()
        return pptx

    def size(self):
        files = self.files()
        return sum([file.size for file in files])

    def extensions(self):
        files = self.files()
        return ", ".join([file.type for file in files])

    def sequence(self):
        folder = Folder.objects.filter(id=self.folder.id).first()
        return folder.sequence()

    class Meta:
        ordering = ["-id"]


class File(models.Model):
    file = models.FileField(upload_to="media/files")
    name = models.CharField(blank=True, null=True)
    size = models.FloatField()
    type = models.CharField()
    package = models.ForeignKey(
        FilePackage, on_delete=models.CASCADE, related_name="file"
    )

    def sequence(self):
        package = FilePackage.objects.filter(id=self.package.id).first()
        return package.sequence()

    def __str__(self):
        return self.name if self.name else self.package.name
