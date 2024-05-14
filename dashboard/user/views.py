from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from account.models import User


class UserListView(ListView):
    model = User
    template_name = 'dashboard/user/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_user"] = User.objects.filter(is_admin=False, is_staff=False).count()
        context["male_user"] = User.objects.filter(is_admin=False, is_staff=False, gender='male').count()
        context["female_user"] = User.objects.filter(is_admin=False, is_staff=False, gender='female').count()
        context["free_user"] = User.objects.filter(is_admin=False, is_staff=False, membership__isnull=True).count()
        context["premium_user"] = User.objects.filter(is_admin=False, is_staff=False, membership__isnull=False).count()
        return context

    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=False)

def UserSearchView(request):
    data = request.POST
    all = data.get("all")
    membership = data.get("membership")
    gender = data.get("gender")
    keyword = data.get('keyword')
    users = User.objects.filter(is_admin=False, is_staff=False)
    
    if membership is not None:
        if membership == "premium":
            users = users.filter(membership__isnull=False)
        else:
            users = users.filter(membership__isnull=True)

    if gender is not None:
        if gender == "male":
            users = users.filter(gender="male")
        else:
            users = users.filter(gender="female")

    if keyword:
        users = users.filter(Q(full_name__icontains=keyword) | Q(email__icontains=keyword) | Q(phone__icontains=keyword))


    context = {
        "user_list": users
    }
    return render(request, 'dashboard/user/search_result.html', context=context)
    
