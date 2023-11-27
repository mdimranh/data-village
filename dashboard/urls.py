from django.urls import path

from .user.urls import urlpatterns as user_urlpattern
from .views import *

urlpatterns = [
    path("", Dashboard)
] + user_urlpattern
