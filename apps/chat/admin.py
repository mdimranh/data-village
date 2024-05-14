from django.contrib import admin

from .models import Chat, Room

admin.site.register(Chat)

class RoomAdmin(admin.ModelAdmin):
    list_display = ["roomid", "name", "created_at", "last_updated"]

admin.site.register(Room, RoomAdmin)
