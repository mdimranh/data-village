from django.urls import path

from .views import *

urlpatterns = [
    path("data", DataView, name="data-view"),
    path("data/<int:fid>", SubFolder, name="sub-folder"),
    path("folder", DeleteFolder, name="delete-folder"),
]
