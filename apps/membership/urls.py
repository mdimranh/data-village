from django.urls import path

from .views import Pricing

urlpatterns = [
    path("pricing", Pricing)
]