from django.shortcuts import render
from django.views.generic import ListView
from apps.course.models import Course
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CourseListView(ListView):
    model = Course
    template_name = 'dashboard/course/courses.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.all()


class CouseAddView(View):
    def get(self, request):
        context = {}
        id = request.GET.get('id')
        if id:
            course = Course.objects.filter(id=id).first()
            context = {
                "course": course
            }
        return render(
            request,
            "dashboard/course/add.html",
            context
        )

    def post(self, request, *args, **kwargs):
        id = request.GET.get("id")
        data = request.POST
        title = data.get("title")
        thumbnail = request.FILES.get("thumbnail")
        class_type = data.get("class_type")
        print(data.get("class_start"))
        start_class = data.get("class_start").split("/")
        class_start = f"{start_class[2]}-{start_class[0]}-{start_class[1]}"
        free = data.get("free") == 'true'
        fee = data.get("fee")
        discount_amount = data.get("discount_amount")
        discount_type = data.get("discount_type")
        if id:
            course = Course.objects.filter(id=id).first()
            course.title=title
            if thumbnail:
                course.thumbnail=thumbnail
            course.class_type = class_type
            course.class_start=class_start
            course.free=free
            if fee.isnumeric():
                course.fee=fee
            course.discount_amount=discount_amount
            course.discount_type=discount_type
        else:
            course = Course(
                title=title,
                thumbnail=thumbnail,
                class_type = class_type,
                class_start=class_start,
                free=free,
                fee=fee if fee.isnumeric() else 0,
                discount_amount=discount_amount if fee.discount_amount() else 0,
                discount_type=discount_type
            )
        course.save()
        courses = Course.objects.all()

        paginator = Paginator(courses, 12)
        page = 1
        try:
            course_list = paginator.page(page)
        except PageNotAnInteger:
            course_list = paginator.page(1)
        except EmptyPage:
            course_list = paginator.page(paginator.num_pages)

        context = {
            "course_list": course_list
        }
        return render(request, 'dashboard/course/course_list.html', context)


class CouseDeleteView(View):
    def delete(self, request):
        id = request.GET.get('id')
        if id:
            course = Course.objects.filter(id=id).first()
            if course:
                course.delete()
        courses = Course.objects.all()

        paginator = Paginator(courses, 12)
        page = 1
        try:
            course_list = paginator.page(page)
        except PageNotAnInteger:
            course_list = paginator.page(1)
        except EmptyPage:
            course_list = paginator.page(paginator.num_pages)

        context = {
            "course_list": course_list
        }
        return render(request, 'dashboard/course/course_list.html', context)