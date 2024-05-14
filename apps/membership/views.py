from django.shortcuts import render

from .models import Pricing


def PricingView(request):
    pricings = Pricing.objects.all()
    context = {
        "memberships": pricings
    }
    return render(request, "pricing.html", context)