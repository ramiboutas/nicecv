from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from ..models.plans import PremiumPlan
from .payments import create_stripe_session
from cms.models.snippets import FrequentAskedQuestion
from ..country import get_country


def plan_list(request):
    c = get_country(request)
    faqs = FrequentAskedQuestion.objects.filter(active=True, category="pricing")
    context = {"plans": PremiumPlan.objects.all(), "faqs": faqs}
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
