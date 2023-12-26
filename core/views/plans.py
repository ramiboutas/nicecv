import json
import logging

import stripe
from djstripe import settings as djstripe_settings

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from ..models.plans import PremiumPlan
from ..models.users import User
from ..models.users import UserPremiumPlan
from .payments import create_stripe_session
from cms.models.snippets import FrequentAskedQuestion

logger = logging.getLogger(__name__)


stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY


def plan_list(request):
    context = {
        "plans": PremiumPlan.objects.all(),
        "faqs": FrequentAskedQuestion.objects.filter(active=True, category="pricing"),
    }
    return render(request, "plans/plan_list.html", context)


@login_required
def plan_detail(request, id):
    plan = get_object_or_404(PremiumPlan, id=id)
    context = {"plan": plan}
    return render(request, "plans/detail.html", context)


def payment_success(request):  # pragma: no cover
    messages.success(request, _("Thank you for your order, enjoy the premium!"))
    return redirect("profile_list")


def payment_fail(request):  # pragma: no cover
    messages.error(request, _("Unexpected error happened, please try again."))
    return redirect("plan_list")


@login_required
def checkout(request, id):  # pragma: no cover
    plan = get_object_or_404(PremiumPlan, id=id)
    checkout_session = create_stripe_session(request, plan)
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):  # pragma: no cover
    payload = request.body
    sig_header = request.headers["stripe-signature"]
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # Retrieve the session. If you require line items in the response,
        # you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event["data"]["object"]["id"],
            expand=["line_items"],
        )
        _ = session.line_items

        data = json.loads(payload)
        plan_id = data["data"]["object"]["metadata"]["plan_id"]
        user_id = data["data"]["object"]["metadata"]["user_id"]
        try:
            user = User.objects.get(id=user_id)
            plan = PremiumPlan.objects.get(id=plan_id)
        except (User.DoesNotExist, PremiumPlan.DoesNotExist):
            return payment_fail(request)

        UserPremiumPlan.objects.create(plan=plan, user=user)

    # Passed signature verification
    return HttpResponse(status=200)
