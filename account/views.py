import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django_htmx.http import HttpResponseClientRedirect
from user_sessions.models import Session

from services.sendEmail import SendVerificationMail

from .models import User

g = GeoIP2()

from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.core import signing
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from account.models import User, Verify
from utils.verify import Messaging


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        context = {"login": True}
        return render(request, "login.html", context=context)

    def post(self, request):
        if request.htmx:
            identity = request.POST.get("full_phone")
            password = request.POST.get("password")
            errors = {}
            if not identity:
                errors.update({"identity": "This field is required."})
            if not password:
                errors.update({"password": "This field is required."})
            if errors:
                return render(
                    request,
                    "component/forms/login.html",
                    {"errors": errors, **request.POST.dict(), "login": True},
                )
            user = User.objects.filter(Q(email=identity) | Q(phone=identity)).first()
            if user is None:
                return render(
                    request,
                    "component/forms/login.html",
                    {
                        "errors": {"message": "User not found with this credential."},
                        **request.POST.dict(),
                        "login": True,
                    },
                )
            print(user.password)
            print(user.check_password(password))
            if user.check_password(password):
                login(request, user)
                return HttpResponseClientRedirect(request.GET.get("redirect", ""))
            return render(
                request,
                "component/forms/login.html",
                {
                    "errors": {"password": "Password is incorrect."},
                    **request.POST.dict(),
                    "login": True,
                },
            )
        context = {
            "login": True,
            "identity": identity,
            "password": password,
        }
        return render(request, "login.html", context)


class Crypto:
    def encrypt(self, data, dump=False):
        if dump:
            data = json.dumps(data)
        return signing.dumps(data)

    def decrypt(self, data, load=False):
        data = signing.loads(data)
        if load:
            return json.loads(data)
        return data


class Signup(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        context = {"login": False}
        return render(request, "login.html", context=context)

    def post(self, request):
        error = {}
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        if not full_name:
            error.update({"phone": "This field is required."})
        if not email:
            error.update({"email": "This field is required."})
        if not password:
            error.update({"password": "This field is required."})
        if error:
            return render(
                request,
                "component/forms/signup.html",
                {"errors": error, **request.POST.dict(), "login": False},
            )
        if User.objects.filter(email=email).exists():
            error["email"] = "User already exists with this email."
        phone = request.POST.get("full_phone")
        if User.objects.filter(phone=phone).exists():
            error["phone"] = "User already exists with this phone."
        if error:
            context = {
                "full_name": full_name,
                "email": email,
                "phone": request.POST.get("phone"),
                "full_phone": request.POST.get("full_phone"),
                "password": password,
                "gender": gender,
                "login": False,
                "errors": error,
            }
            return render(request, "component/forms/signup.html", context=context)
        user = User(email=email, phone=phone, full_name=full_name, is_active=False)
        user.save()
        user.set_password(password)
        user.save()
        verify = Verify(user=user)
        verify.save()
        body = f"Hi {full_name}, Your pemis verification code is {verify.phone_code}."
        # messaging = Messaging().send(body=body, to=phone)
        # SendVerificationMail(request, user_id=user.id, code=verify.email_code)
        secret = Crypto().encrypt({"phone": phone, "email": email}, True)
        redirect_url = reverse("verify", kwargs={"secret": secret})
        return HttpResponseClientRedirect(redirect_url)
        # return redirect(reverse("phone-verify", kwargs={"secret": secret}))


class VerifyView(View):
    def mask_phone(self, phone):
        if len(phone) < 4:
            return phone
        else:
            return "*" * (len(phone) - 4) + phone[-4:]

    def get(self, request, *args, **kwargs):
        secret = kwargs.get("secret")
        data = Crypto().decrypt(secret, True)
        phone = data.get("phone")
        get_user = User.objects.get(phone=phone)
        verify = Verify.objects.filter(user=get_user).first()
        if not verify.phone_verified:
            context = {
                "phone": self.mask_phone(str(get_user.phone)),
                "secret": secret,
            }
            return render(request, "verify/phone-otp.html", context=context)
        elif not verify.email_verified:
            context = {
                "email": self.mask_phone(str(get_user.email)),
                "secret": secret,
            }
            return render(request, "verify/email-otp.html", context=context)

    # def post(self, request, *args, **kwargs):
    #     secret = kwargs.get("secret", "")
    #     phone = Crypto().decrypt(secret)
    #     get_user = User.objects.get(phone=phone)
    #     verify_data = Verify.objects.get(user=get_user)
    #     if verify_data.phone_verified:
    #         if verify_data.email_verified:
    #             return
    #     otp = ""
    #     for i in range(1, 7):
    #         otp += request.POST.get(f"d{i}", "")
    #     if verify_data.phone_code == otp:
    #         if verify_data.phone_code_expired < timezone.now():
    #             context = {
    #                 "error": "Code is expired.",
    #                 "phone": self.mask_phone(str(get_user.phone)),
    #                 "secret": self.encrypt(str(get_user.phone)),
    #             }
    #             return render(request, "verify/phone-otp-card.html", context=context)
    #         verify_data.phone_verified = True
    #         verify_data.email_code_expired = timezone.now()
    #         verify_data.save()
    #         secret = Crypto().encrypt(get_user.email)
    #         return redirect(reverse("email-verify", kwargs={"secret": secret}))
    #     else:
    #         context = {
    #             "error": "Code is incorrect.",
    #             "phone": self.mask_phone(str(get_user.phone)),
    #             "secret": self.encrypt(str(get_user.phone)),
    #         }
    #         return render(request, "verify/phone-otp-card.html", context=context)


class PhoneVerify(View):
    def mask_phone(self, phone):
        if len(phone) < 4:
            return phone
        else:
            return "*" * (len(phone) - 4) + phone[-4:]

    def mask_email(self, email):
        if len(email) < 4:
            return email
        else:
            return email[0:4] + "*" * (len(email) - 4)

    def post(self, request, *args, **kwargs):
        secret = kwargs.get("secret", "")
        data = Crypto().decrypt(secret, True)
        phone = data.get("phone")
        get_user = User.objects.get(phone=phone)
        verify_data = Verify.objects.get(user=get_user)
        if verify_data.phone_verified:
            context = {"email": get_user.email, "secret": secret}
            return render(request, "verify/email-otp-card.html", context=context)
        otp = ""
        for i in range(1, 7):
            otp += request.POST.get(f"d{i}", "")
        if verify_data.phone_code == otp:
            if verify_data.phone_code_expired < timezone.now():
                context = {
                    "error": "Code is expired.",
                    "phone": self.mask_phone(str(get_user.phone)),
                    "secret": secret,
                }
                return render(request, "verify/phone-otp-card.html", context=context)
            verify_data.phone_verified = True
            # verify_data.email_code_expired = timezone.now()
            verify_data.save()
            return render(
                request,
                "verify/email-otp-card.html",
                {"email": self.mask_email(get_user.email), "secret": secret},
            )
        else:
            context = {
                "error": "Code is incorrect.",
                "phone": self.mask_phone(str(get_user.phone)),
                "secret": secret,
            }
            return render(request, "verify/phone-otp-card.html", context=context)


class EmailVerify(View):
    def mask_email(self, email):
        if len(email) < 4:
            return email
        else:
            return email[0:4] + "*" * (len(email) - 4)

    def post(self, request, *args, **kwargs):
        secret = kwargs.get("secret", "")
        data = Crypto().decrypt(secret, True)
        email = data.get("email")
        get_user = User.objects.get(email=email)
        verify_data = Verify.objects.get(user=get_user)
        otp = ""
        for i in range(1, 7):
            otp += request.POST.get(f"d{i}", "")
        if verify_data.email_code == otp:
            if verify_data.email_code_expired < timezone.now():
                context = {
                    "error": "Code is expired.",
                    "email": self.mask_email(str(get_user.email)),
                    "secret": secret,
                }
                return render(request, "verify/email-otp-card.html", context=context)
            verify_data.email_verified = True
            verify_data.save()
            get_user.is_active = True
            get_user.save()
            return HttpResponseClientRedirect(reverse("login"))
        else:
            context = {
                "error": "Code is incorrect.",
                "email": self.mask_email(str(get_user.email)),
                "secret": secret,
            }
            return render(request, "verify/email-otp-card.html", context=context)


def logout_view(request):
    logout(request)
    return redirect("home")


def check_expired(session):
    session.expired = session.expire_date < timezone.now()
    return session


@login_required
def UserProfile(request):
    sessions = Session.objects.filter(user=request.user).exclude(
        session_key=request.session._SessionBase__session_key
    )
    sessions = list(map(check_expired, sessions))
    current = Session.objects.filter(
        session_key=request.session._SessionBase__session_key
    ).first()
    context = {"sessions": sessions, "current": current}
    return render(request, "profile/profile.html", context=context)


@login_required
def removeSessions(request, key):
    if key == "all":
        Session.objects.filter(user=request.user).exclude(
            session_key=request.session._SessionBase__session_key
        ).update(expire_date=timezone.now())
    else:
        Session.objects.filter(user=request.user, session_key=key).update(
            expire_date=timezone.now()
        )
    sessions = Session.objects.filter(user=request.user).exclude(
        session_key=request.session._SessionBase__session_key
    )
    sessions = list(map(check_expired, sessions))
    current = Session.objects.filter(
        session_key=request.session._SessionBase__session_key
    ).first()
    context = {"sessions": sessions, "current": current}
    return render(request, "profile/sections/sessions.html", context=context)


# @login_required
# def UserList(request):
#     # users = User.objects.all().exclude(id=request.user.id)
#     users = User.objects.all()
#     context = {
#         "users": users
#     }
#     return render(request, "users/users.html", context=context)


class UserList(ListView):
    model = User
    template_name = "users/users.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            User.objects.all().exclude(id=self.request.user.id).exclude(is_admin=True)
        )


class UserSearch(ListView):
    model = User
    template_name = "users/user_section.html"
    paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get("keyword", "")
        if keyword == "":
            queryset = (
                User.objects.all()
                .exclude(id=self.request.user.id)
                .exclude(is_admin=True)
            )
        else:
            queryset = (
                User.objects.filter(full_name__icontains=keyword)
                .exclude(id=self.request.user.id)
                .exclude(is_admin=True)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keyword"] = self.request.GET.get("keyword", "")
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
