from django.shortcuts import render

from .models import Membership


def Pricing(request):
    memberships = Membership.objects.all()
    context = {
        "memberships": memberships
    }
    return render(request, "pricing.html", context)