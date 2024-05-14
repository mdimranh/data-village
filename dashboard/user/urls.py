from django.urls import path

from .message import *
from .views import *

urlpatterns = [
    path("users", UserListView.as_view()),
    path("user/search", UserSearchView),
    path("messages", MessageListView.as_view()),
]
