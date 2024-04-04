from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_lib import SSLCOMMERZ
from django.contrib.auth.decorators import login_required
from account.models import User
from apps.membership.models import Membership, Pricing

from .models import Payment

settings = {
    "store_id": "pte6564c943b9553",
    "store_pass": "pte6564c943b9553@ssl",
    "issandbox": True,
}

@login_required(login_url="/login")
def PaymentView(request, id):
    pricing = Pricing.objects.get(id=id)
    tid = (
        "DV-"
        + timezone.now().strftime("%d%m%y")
        + "-"
        + timezone.now().strftime("%H%M%S")
    )
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body["total_amount"] = pricing.price
    post_body["currency"] = "BDT"
    post_body["tran_id"] = tid
    post_body["success_url"] = (
        f"http://{request.get_host()}/payment/success/{request.user.id}/{pricing.id}"
    )
    post_body["fail_url"] = "http://{request.get_host()}/payment/fail"
    post_body["cancel_url"] = "http://{request.get_host()}/payment/cancel"
    post_body["emi_option"] = 0
    post_body["cus_name"] = request.user.full_name
    post_body["cus_email"] = request.user.email
    post_body["cus_phone"] = "01700000000"
    post_body["cus_add1"] = "Dhaka, Bangladesh"
    post_body["cus_city"] = "Dhaka"
    post_body["cus_country"] = "Bangladesh"
    post_body["shipping_method"] = "NO"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = 1
    post_body["product_name"] = "Test"
    post_body["product_category"] = "Test Category"
    post_body["product_profile"] = "general"
    response = sslcommez.createSession(post_body)
    return redirect(response.get("redirectGatewayURL", "/"))
    return redirect("pricing")


@csrf_exempt
def PaymentSuccess(request, uid, pid):
    data = request.POST

    user = User.objects.get(id=uid)
    pricing = Pricing.objects.get(id=pid)

    payment_data = {}
    payment_data["tran_id"] = data.get("tran_id")
    payment_data["val_id"] = data.get("val_id")
    payment_data["amount"] = data.get("amount")
    payment_data["store_amount"] = data.get("store_amount")
    payment_data["card_type"] = data.get("card_type")
    payment_data["card_no"] = data.get("card_no")
    payment_data["bank_tran_id"] = data.get("bank_tran_id")
    payment_data["status"] = data.get("status")

    payment = Payment(**payment_data)
    payment.save()

    membership = Membership(payment=payment, user=user, pricing=pricing)
    membership.save()

    return redirect("home")


@csrf_exempt
def PaymentCancel(request):
    data = request.POST
    print("--------- Cancel ---------")
    print(data)
    return redirect("pricing")


@csrf_exempt
def PaymentFail(request):
    data = request.POST
    print("--------- Fail ---------")
    print(data)
    return redirect("pricing")
