from django.urls import path

from .views import datas

urlpatterns = [
    path('datas/<str:type>', datas)
]