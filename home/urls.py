from django.urls import path

from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('privacy', PrivacyView, name='privacy'),
    path('refund/policy', RefundPolicyView, name='refund_policy'),
    path('dashboard', DashboardList.as_view(), name='dashboard')
]