from django.urls import path

from .message import *
from .views import *

urlpatterns = [
    path("users", UserListView.as_view()),
    path("user/search", UserSearchView.as_view()),
    path("messages", MessageListView.as_view()),
]
