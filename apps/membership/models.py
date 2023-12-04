from django.db import models
from django_jsonform.models.fields import ArrayField

from account.models import User
from apps.payment.models import Payment

# from .

class Pricing(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    options = ArrayField(models.CharField(max_length=255), size=10)

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='membership')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    pricing = models.ForeignKey(Pricing, on_delete=models.SET_NULL, null=True)
