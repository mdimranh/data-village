from django.shortcuts import render
from django.views import View

from .models import Message


class ContactUSView(View):
    def get(self, request):
        return render(request=request, template_name="contact-us.html", context={})

    def post(self, request):
        data = request.POST
        email = data.get("email")
        subject = data.get("subject")
        body = data.get("body")
        message = Message(email=email, subject=subject, body=body)
        message.save()
        context = {"success": "Message created successfully"}
        return render(
            request=request,
            template_name="component/message_form.html",
            context=context,
        )
