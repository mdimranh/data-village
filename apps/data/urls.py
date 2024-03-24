from django.urls import path

from .views import *

urlpatterns = [path("datas/<str:type>", datas), path("data/<str:type>", data)]
