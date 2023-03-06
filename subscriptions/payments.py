import stripe
from django.conf import settings
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from .models import Order
from .models import Plan
from accounts.models import CustomUser

def fulfill_order(user_id: int = None, plan_id: int = None):
    # fulfills the order and assigns premium to user.
    # returns False if the order was not fulfilled.
    # returns True if the order was fulfilled.
    proceed = user_id is not None and plan_id is not None

    if not proceed:
        return False

    try:
        plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        return False
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return False
    
    Order(plan=plan, user=user).save()
    user.set_paid_until(plan.months)
    return True

def create_stripe_session(request, plan: Model):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        # customer_email = request.user.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "EUR",
                    "product_data": {
                        "name": str(plan.months)
                        + _(" months subscription to premium (no renewal)"),
                    },
                    "unit_amount": int(plan.price * 100),
                },
                "quantity": 1,
            },
        ],
        metadata={"plan_id": plan.id, "user_id": request.user.id},
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payments_success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("payments_failed")),
    )
    return session
