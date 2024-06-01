from django.shortcuts import render
from account.models import User
from .models import Privacy, RefundPolicy, TermsCondition
from apps.payment.models import Payment
from django.db.models import Sum
from datetime import datetime, timedelta


def Dashboard(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    total_amount = Payment.objects.aggregate(Sum('store_amount')).get("store_amount__sum")
    total_amount_last_30_days = Payment.objects.filter(tran_date__range=[start_date, end_date]).aggregate(Sum('store_amount')).get("store_amount__sum")

    total_user_last_30_days = User.objects.filter(date_joined__range=[start_date, end_date], is_superuser=False, is_active=True).count()

    student = User.objects.filter(is_superuser=False, is_active=True, designation="student").count()
    teacher = User.objects.filter(is_superuser=False, is_active=True, designation="teacher").count()
    corporate = User.objects.filter(is_superuser=False, is_active=True, designation="corporate").count()

    total_user = student+teacher+corporate

    context = {
        "user": {
            "total": total_user,
            "last_month": round((total_user_last_30_days / total_user) * 100, 2),
            "category": {
                "student": round((student / total_user) * 100, 2),
                "teacher": round((teacher / total_user) * 100, 2),
                "corporate": round((corporate / total_user) * 100, 2)
            }
        },
        "revenue": {
            "total": total_amount,
            "last_month": round((total_amount_last_30_days / total_amount) * 100, 2)
        }
    }
    return render(request, "dashboard/dashboard/home.html", context)


def PrivacyView(request):
    if request.method == "GET":
        privacy = Privacy.objects.first()
        if privacy is None:
            privacy = Privacy.objects.create(body="")
        context = {"privacy": privacy}
        return render(request, "dashboard/meta/privacy.html", context=context)
    if request.method == "POST":
        body = request.POST.get("body")
        editor_content = request.POST.get("editor_content")
        privacy = Privacy.objects.first()
        if privacy is None:
            privacy = Privacy.objects.create(body=editor_content)
        else:
            privacy.body = editor_content
            privacy.save()
        context = {"privacy": privacy}
        return render(request, "dashboard/meta/privacy.html", context=context)


def RefundPolicyView(request):
    if request.method == "GET":
        refund_policy = RefundPolicy.objects.first()
        if refund_policy is None:
            refund_policy = RefundPolicy.objects.create(body="")
        context = {"privacy": refund_policy}
        return render(request, "dashboard/meta/refund_policy.html", context=context)
    if request.method == "POST":
        body = request.POST.get("body")
        editor_content = request.POST.get("editor_content")
        refund_policy = RefundPolicy.objects.first()
        if refund_policy is None:
            refund_policy = RefundPolicy.objects.create(body=editor_content)
        else:
            refund_policy.body = editor_content
            refund_policy.save()
        context = {"privacy": refund_policy}
        return render(request, "dashboard/meta/refund_policy.html", context=context)


def TermsConditionView(request):
    if request.method == "GET":
        terms_condition = TermsCondition.objects.first()
        if terms_condition is None:
            terms_condition = TermsCondition.objects.create(body="")
        context = {"terms": terms_condition}
        return render(request, "dashboard/meta/terms-condition.html", context=context)
    if request.method == "POST":
        body = request.POST.get("body")
        editor_content = request.POST.get("editor_content")
        terms_condition = TermsCondition.objects.first()
        if terms_condition is None:
            terms_condition = TermsCondition.objects.create(body=editor_content)
        else:
            terms_condition.body = editor_content
            terms_condition.save()
        context = {"terms": terms_condition}
        return render(request, "dashboard/meta/terms-condition.html", context=context)