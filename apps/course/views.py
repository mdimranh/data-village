from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Course


class CourseList(ListView):
    model = Course
    template_name = "courses.html"
    paginate_by = 1


class CourseDetails(DetailView):
    model = Course
    template_name = "course.html"
