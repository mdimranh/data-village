from django.shortcuts import render

from .models import Privacy, RefundPolicy, TermsCondition


def Dashboard(request):
    return render(request, "dashboard/dashboard/home.html")


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