from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Course


class CourseList(ListView):
    model = Course
    template_name = "courses.html"
    paginate_by = 1
