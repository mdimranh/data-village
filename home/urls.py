from django.urls import path

from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('login', Login.as_view(), name='login'),
    path('signup', Signup.as_view(), name='signup'),
    path('logout', logout_view, name='logout'),
    path('pricing', Pricing, name='pricing'),
    path('dashboard', DashboardList.as_view(), name='dashboard'),
    path('phone/verify/<secret>', PhoneVerify.as_view(), name='phone-verify'),
    path('email/verify/<secret>', EmailVerify.as_view(), name='email-verify')
]