from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.core import signing
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from account.models import User, Verify
from dashboard.models import Privacy
from utils.verify import Messaging


def Home(request):
    return render(request, 'home.html')

class DashboardList(ListView):
    model = User
    template_name = "dashboard.html"

def PrivacyView(request):
    privacy = Privacy.objects.first()
    context = {"privacy": privacy}
    return render(request, 'privacy.html', context)