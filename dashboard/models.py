from ckeditor.fields import RichTextField
from django.db import models
from django.forms import ModelForm


class Privacy(models.Model):
    # body = models.TextField()
    body = RichTextField()

class PrivacyForm(ModelForm):
    class Meta:
        model = Privacy
        fields = "__all__"
