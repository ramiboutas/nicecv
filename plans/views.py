import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from .models import Plan
from .models import PlanFAQ
from .payments import create_stripe_session
from .payments import fulfill_order


def plan_list(request):
    context = {
        "plans": Plan.objects.all(),
        "FAQs": PlanFAQ.objects.filter(active=True),
    }
    return render(request, "plans/plan_list.html", context)


@login_required
def payment_success_view(request):
    print(request.GET.get("session_id"))
    messages.success(request, _("Thank you for your order, enjoy the premium!"))
    return redirect("home")


@login_required
def payment_failed_view(request):
    messages.error(request, _("Unexpected error happened, please try again."))
    return redirect("plans_plans")


def paypal_checkout_view():
    pass


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
