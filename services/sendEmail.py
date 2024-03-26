from control.emailconfig import backend
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string


def SendVerificationMail(request):
    site = get_current_site(request)
    email_config = EmailConfig.objects.get()
    email = user.email
    subject, from_email, to = "Email Verification", email_config.email_host_user, email
    text_content = "Email Verification"
    html_content = render_to_string(
        "email/verification.html",
        context={
            "user": user.first_name + " " + user.last_name,
            "domain": get_current_site(request).domain,
            "siteinfo": siteinfo,
            "activation_key": euser.activation_key,
        },
    )
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to], connection=backend
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
