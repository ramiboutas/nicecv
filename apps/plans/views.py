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


def plan_list_view(request):
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


def payment_success_view(request):  # pragma: no cover
    messages.success(request, _("Thank you for your order, enjoy the premium!"))
    return redirect("core:home")


def payment_fail_view(request):  # pragma: no cover
    messages.error(request, _("Unexpected error happened, please try again."))
    return redirect("plans:list")


@login_required
def checkout_view(request, id):  # pragma: no cover
    plan = get_object_or_404(PremiumPlan, id=id)
    checkout_session = create_stripe_session(request, plan)
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook_view(request):  # pragma: no cover
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
