import json
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from djstripe import settings as djstripe_settings

logger = logging.getLogger(__name__)


User = get_user_model()
stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY


from .models import PremiumPlan
from .models import PlanFAQ
from .payments import create_stripe_session
from .payments import fulfill_order


def plan_list(request):
    context = {
        "plans": PremiumPlan.objects.all(),
        "faqs": PlanFAQ.objects.filter(active=True),
    }
    return render(request, "plans/plan_list.html", context)


@login_required
def plan_detail_view(request, id):
    plan = get_object_or_404(PremiumPlan, id=id)
    context = {"plan": plan}
    return render(request, "plans/detail.html", context)


def payment_success_view(request):
    messages.success(request, _("Thank you for your order, enjoy the premium!"))
    return redirect("core:home")


def payment_failed_view(request):
    messages.error(request, _("Unexpected error happened, please try again."))
    return redirect("plans:list")


@login_required
def checkout_view(request, id):
    plan = get_object_or_404(PremiumPlan, id=id)
    checkout_session = create_stripe_session(request, plan)
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event["data"]["object"]["id"],
            expand=["line_items"],
        )

        line_items = session.line_items

        data = json.loads(payload)
        plan_id = data["data"]["object"]["metadata"]["plan_id"]
        user_id = data["data"]["object"]["metadata"]["user_id"]
        fulfill_order(user_id=user_id, plan_id=plan_id)

    # Passed signature verification
    return HttpResponse(status=200)


# b'{\n  "id": "evt_1MkxUOIeF8oCm2lonff14M3I",\n  "object": "event",\n  "api_version": "2020-08-27",\n  "created": 1678660540,\n  "data": {\n    "object": {\n      "id": "cs_test_a16punzK4ihyktWcjzOG0eIavHzIPiNjVjrFIAA0KPuTLpFreZhgc4JT8D",\n      "object": "checkout.session",\n      "after_expiration": null,\n      "allow_promotion_codes": null,\n      "amount_subtotal": 1000,\n      "amount_total": 1000,\n      "automatic_tax": {\n        "enabled": false,\n        "status": null\n      },\n      "billing_address_collection": null,\n      "cancel_url": "http://127.0.0.1:8000/",\n      "client_reference_id": null,\n      "consent": null,\n      "consent_collection": null,\n      "created": 1678660508,\n      "currency": "eur",\n      "custom_fields": [\n\n      ],\n      "custom_text": {\n        "shipping_address": null,\n        "submit": null\n      },\n      "customer": "cus_NVzTrA9clOEYdB",\n      "customer_creation": "always",\n      "customer_details": {\n        "address": {\n          "city": null,\n          "country": "DE",\n          "line1": null,\n          "line2": null,\n          "postal_code": null,\n          "state": null\n        },\n        "email": "learnmatlabwithrami@gmail.com",\n        "name": "a",\n        "phone": null,\n        "tax_exempt": "none",\n        "tax_ids": [\n\n        ]\n      },\n      "customer_email": null,\n      "expires_at": 1678746908,\n      "invoice": null,\n      "invoice_creation": {\n        "enabled": false,\n        "invoice_data": {\n          "account_tax_ids": null,\n          "custom_fields": null,\n          "description": null,\n          "footer": null,\n          "metadata": {\n          },\n          "rendering_options": null\n        }\n      },\n      "livemode": false,\n      "locale": null,\n      "metadata": {\n        "plan_id": "1",\n        "user_id": "1",\n        "djstripe_subscriber": "1"\n      },\n      "mode": "payment",\n      "payment_intent": "pi_3MkxTsIeF8oCm2lo1bE4xmPO",\n      "payment_link": null,\n      "payment_method_collection": "always",\n      "payment_method_options": {\n      },\n      "payment_method_types": [\n        "card"\n      ],\n      "payment_status": "paid",\n      "phone_number_collection": {\n        "enabled": false\n      },\n      "recovered_from": null,\n      "setup_intent": null,\n      "shipping": null,\n      "shipping_address_collection": null,\n      "shipping_options": [\n\n      ],\n      "shipping_rate": null,\n      "status": "complete",\n      "submit_type": null,\n      "subscription": null,\n      "success_url": "http://127.0.0.1:8000/plans/success/?session_id={CHECKOUT_SESSION_ID}",\n      "total_details": {\n        "amount_discount": 0,\n        "amount_shipping": 0,\n        "amount_tax": 0\n      },\n      "url": null\n    }\n  },\n  "livemode": false,\n  "pending_webhooks": 2,\n  "request": {\n    "id": null,\n    "idempotency_key": null\n  },\n  "type": "checkout.session.completed"\n}'
