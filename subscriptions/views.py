import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View

from .models import Order
from .models import Plan
from .payments import create_stripe_session

User = get_user_model()


def plan_list(request):
    months = getattr(request.GET, "months", 2)
    plan = Plan.objects.get(default=True)
    month_list = Plan.objects.values_list("months", flat=True)
    context = {"plan": plan, "months": month_list}
    return render(request, "subscriptions/plan_list.html", context)


@login_required
def hx_get_payment_methods_view(request):
    if request.htmx:
        return render(request, "subscriptions/partials/payment-methods.html")
    return redirect("subscriptions_plans")


def hx_update_price_view(request):
    if request.htmx:
        months = request.GET.get("months")
        plan = Plan.objects.get(months=int(months))
        context = {"plan": plan}
        return render(request, "subscriptions/partials/price.html", context)
    return redirect("subscriptions_plans")


@login_required
def payment_success_view(request):
    print(request.GET.get("session_id"))
    messages.success(request, _("Thank you for your order, enjoy the premium!"))
    return redirect("home")


@login_required
def payment_failed_view(request):
    messages.error(request, _("Unexpected error happened, please try again."))
    return redirect("subscriptions_plans")


@login_required
@require_POST
def proceed_with_payment_view(request):
    payment_method = request.POST.get("payment_method")

    if payment_method == "card":
        return stripe_checkout_view(request)

    elif payment_method == "paypal":
        return paypal_checkout_view(request)

    elif payment_method == "coinbase":
        return coinbase_checkout_view(request)

    messages.error(request, _("Somethig wrong happened, please try again or later"))
    return redirect("subscriptions_plans")


@login_required
def stripe_checkout_view(request):
    months = request.POST.get("months")
    plan = Plan.objects.filter(months=months).first()
    checkout_session = create_stripe_session(request, plan)
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:  # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:  # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        # this means the event is comming from stripe
        session = event["data"]["object"]
        plan_id = int(session["metadata"]["plan_id"])
        user_id = int(session["metadata"]["user_id"])
        fulfill_order(user_id=user_id, plan_id=plan_id)
    return HttpResponse(status=200)
