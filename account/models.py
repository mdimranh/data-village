import random
from datetime import datetime, timedelta

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
# from django.utils.http import urlquote
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, phone, password, gender, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email= self.normalize_email(email)
        user = self.model(
                email=email,
                phone=phone,
                gender=gender,
                is_staff=is_staff, is_active=True,
                is_superuser=is_superuser,
                last_login=now,
                date_joined=now,
                **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone=None, password=None, **extra_fields):
        return self._create_user(email, phone, password, False, False, **extra_fields)

    def create_superuser(self, email, phone, password, **extra_fields):
        return self._create_user(email, phone, password, True, True, **extra_fields)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ("others", "other's"),
) 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True, region='BD')
    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    picture = models.ImageField(upload_to="media/user", blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now=True)
    is_active   = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    class Meta:
        verbose_name=_('user')
        verbose_name_plural = ('users')

    # def get_absolute_url(self):
    #     return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    # def email_user(self, subject, message, from_email=None):
    #     send_mail(subject, message, from_email, [self.email])

# @receiver(post_delete, sender=User)
# def delete_file(sender, instance, created, **kwargs):
#     if instance.picture:
#         instance.picture.delete(False)

def GenerateCode(l=6):
    code = ""
    while len(code) != l:
        num = random.randint(0, 9)
        code += str(num)
    return code

def CodeExpire():
    return datetime.now() + timedelta(minutes=30)

class Verify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_code = models.CharField(max_length=10, default=GenerateCode)
    phone_code_expired = models.DateTimeField(default=CodeExpire)
    phone_verified = models.BooleanField(default=False)
    email_code = models.CharField(max_length=10, default=GenerateCode)
    email_code_expired = models.DateTimeField(default=CodeExpire)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email