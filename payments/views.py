import stripe
import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from pricing.models import Plan
from .models import Order

User = get_user_model()
# https://nicecv.online/pricing/payment/stripe/webhook/
# https://testdriven.io/blog/django-coinbase/

def fullfill_order(user_id=None, plan_id=None):
    """
    This function fullfills the order and assignated the premium data
    to the user.
    """
    if user_id != None and plan_id != None:
        plan = Plan.objects.get(id=plan_id)
        user = User.objects.get(id=user_id)
        Order(plan=plan, user=user).save()
        user.set_paid_until(plan.months)


@login_required
def payment_success_view(request):
    print(request.GET.get("session_id"))
    messages.success(request, _('Thank you for your order, enjoy the premium!'))
    return redirect('home')

@login_required
def payment_failed_view(request):
    messages.error(request, _('Unexpected error happened, please try again.'))
    return redirect('pricing_main')


@login_required
@require_POST
def proceed_with_payment_view(request):
    payment_method = request.POST.get('payment_method')

    if payment_method == "card":
        return stripe_checkout_view(request)

    elif payment_method == "paypal":
        return paypal_checkout_view(request)

    elif payment_method == "coinbase":
        return coinbase_checkout_view(request)

    messages.error(request, _('Somethig wrong happened, please try again or later'))
    return redirect('pricing_main')


@login_required
def stripe_checkout_view(request):
    months = request.POST.get('months')
    plan = Plan.objects.filter(months=months).first()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # customer_email = request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'EUR',
                    'product_data': {
                    'name': str(plan.months) + _(' months subscription to premium (no renewal)'),
                    },
                    'unit_amount': int(plan.price * 100),
                },
                'quantity': 1,
            },
        ],
        metadata={"plan_id": plan.id, "user_id": request.user.id},
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payments_success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payments_failed')),
    )

    return redirect(checkout_session.url, code=303)

@csrf_exempt
def stripe_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if event["type"] == "checkout.session.completed":
      # this means the event is comming from stripe
      session = event["data"]["object"]
      plan_id = int(session["metadata"]["plan_id"])
      user_id = int(session["metadata"]["user_id"])
      fullfill_order(user_id=user_id, plan_id=plan_id)
  return HttpResponse(status=200)


def paypal_checkout_view(request):
    return HttpResponse("This wiew will proceed with paypal session")

def coinbase_checkout_view(request):
    return HttpResponse("This wiew will proceed with coinbase session")
