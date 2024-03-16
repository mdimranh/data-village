from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("contactus/", TemplateView.as_view(template_name="contact-us.html")),
    path("aboutus/", TemplateView.as_view(template_name="about-us.html")),
]
