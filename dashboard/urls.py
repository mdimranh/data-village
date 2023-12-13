from django.urls import path

from .data.urls import urlpatterns as data_urlpattern
from .user.urls import urlpatterns as user_urlpattern
from .views import *

urlpatterns = [
    path("", Dashboard),
    path("privacy", PrivacyView),
    path("refund/policy", RefundPolicyView),
] + user_urlpattern + data_urlpattern
