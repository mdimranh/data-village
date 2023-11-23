from django.urls import path

from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('dashboard', DashboardList.as_view(), name='dashboard')
]