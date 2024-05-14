from django import forms
from django.contrib import admin

from .models import Membership, Pricing

# from utils.fields.arrayfield import ArrayFieldWidget



# class MembershipAdminForm(forms.ModelForm):
#     class Meta:
#         model = Membership
#         fields = '__all__'
#         widgets = {
#             'my_array_field': ArrayFieldWidget(),
#         }

# class MembershipAdmin(admin.ModelAdmin):
#     form = MembershipAdminForm

admin.site.register(Pricing)
admin.site.register(Membership)
