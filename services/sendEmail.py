from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string

from account.models import User

# backend = EmailBackend(
#     host=config.email_host,
#     port=config.email_port,
#     username=config.email_host_user,
#     password=config.email_host_password,
#     use_tls=True,
#     fail_silently=True,
# )
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp-relay.brevo.com"
# EMAIL_USE_TLS = False
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = "mdimranh750@gmail.com"
# EMAIL_HOST_PASSWORD = "2EmMpHCnzacBQvGF"


def SendVerificationMail(request, user_id, code):
    user = User.objects.get(id=user_id)
    site = get_current_site(request)
    subject, from_email, to = (
        "Email Verification Code",
        "mdimranh750@gmail.com",
        user.email,
    )
    text_content = "Email Verification"
    html_content = render_to_string(
        "email/verification.html",
        context={"code": code},
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
