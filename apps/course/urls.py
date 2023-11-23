from django.urls import path

from .views import *

urlpatterns = [
    path('courses', CourseList.as_view(), name='courses')
]