from django.urls import path
from django.views.generic import TemplateView

from .views import ContactUSView, MessageDetailView

urlpatterns = [
    # path("contactus/", TemplateView.as_view(template_name="contact-us.html")),
    path("contactus/", ContactUSView.as_view()),
    path("message/<pk>/details", MessageDetailView),
    path("aboutus/", TemplateView.as_view(template_name="about.html")),
]
