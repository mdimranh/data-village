from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from .models import Message
import time


class ContactUSView(View):
    def get(self, request):
        return render(request=request, template_name="contact-us.html", context={})

    def post(self, request):
        data = request.POST
        name = data.get("name")
        email = data.get("email")
        phone = data.get("full_phone")
        subject = data.get("subject")
        body = data.get("body")
        message = Message(name=name, email=email, phone=phone, subject=subject, body=body)
        message.save()
        context = {"success": "Message created successfully"}
        return render(
            request=request,
            template_name="component/message_form.html",
            context=context,
        )

def MessageDetailView(request, pk):
    template_name = "dashboard/message/details.html"
    message = Message.objects.filter(id=pk).first()
    if message is not None:
        message.status = "seen"
        message.save()
    return render(request, template_name, {"message": message})