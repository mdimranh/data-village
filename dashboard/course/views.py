from django.shortcuts import render
from django.views.generic import ListView
from apps.course.models import Course


class CourseListView(ListView):
    model = Course
    template_name = 'dashboard/course/courses.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.all()