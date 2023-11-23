from django.db import models
from django_jsonform.models.fields import ArrayField


class Membership(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    options = ArrayField(models.CharField(max_length=255), size=10)
