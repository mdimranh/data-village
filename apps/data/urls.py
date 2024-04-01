from django.urls import path

from .views import *

urlpatterns = [
    path("datahub", datas),
    path("datahub/<int:id>", datas),
    path("data/<str:type>", data),
]
