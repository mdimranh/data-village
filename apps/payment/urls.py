from django.urls import path

from .views import *

urlpatterns = [
    path("<int:id>", PaymentView, name="payment"),
    path("success/<int:uid>/<int:pid>", PaymentSuccess, name="payment-success"),
    path("cancel", PaymentCancel, name="payment-cancel"),
    path("fail", PaymentFail, name="payment-fail"),
]
