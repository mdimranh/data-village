from django.contrib import admin

from .models import File, Folder, FilePackage

admin.site.register(Folder)
admin.site.register(File)
admin.site.register(FilePackage)
# Register your models here.
