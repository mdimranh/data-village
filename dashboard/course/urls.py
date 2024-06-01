from django.urls import path
from .views import *

urlpatterns = [
    path("course", CourseListView.as_view()),
    path("course/add", CouseAddView.as_view()),
    path("course/delete", CouseDeleteView.as_view())
]
