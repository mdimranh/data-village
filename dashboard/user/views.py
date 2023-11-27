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
        return context

    def get_queryset(self):
        return User.objects.filter(is_admin=False, is_staff=False)
    
