from django.urls import path

from services.sendEmail import SendVerificationMail

from .views import *

urlpatterns = [
    path("datahub", datas),
    path("datahub/<int:id>", datas),
    path("datahub/file/<int:id>", fileView),
    path("datahub/file/<int:id>/download", fileDownload),
    path("data/<str:type>", data),
    path("mail", SendVerificationMail),
]
