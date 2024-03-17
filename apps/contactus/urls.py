from django.urls import path
from django.views.generic import TemplateView

from .views import ContactUSView

urlpatterns = [
    # path("contactus/", TemplateView.as_view(template_name="contact-us.html")),
    path("contactus/", ContactUSView.as_view()),
    path("aboutus/", TemplateView.as_view(template_name="about-us.html")),
]
