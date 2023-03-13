import stripe
from django.urls import reverse
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from djstripe import models as djstripe_models
from djstripe import settings as djstripe_settings

from .models import PremiumPlan
from accounts.models import CustomUser
from accounts.models import UserPremiumPlan


def fulfill_order(user_id: int = None, plan_id: int = None):
    # fulfills the order and assigns premium to user.
    # returns False if the order was not fulfilled.
    # returns True if the order was fulfilled.
    proceed = user_id is not None and plan_id is not None

    if not proceed:
        return False

    try:
        plan = PremiumPlan.objects.get(id=plan_id)
    except PremiumPlan.DoesNotExist:
        return False

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return False

    UserPremiumPlan.objects.create(plan=plan, user=user)
    user.set_plan(plan)
    return True


def create_stripe_session(request, plan: Model):
    """
    Creates and returns a Stripe Checkout Session
    """

    success_url = (
        request.build_absolute_uri(reverse("plans:success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )

    cancel_url = request.build_absolute_uri(reverse("core:home"))

    # get the id of the Model instance of djstripe_settings.djstripe_settings.get_subscriber_model()
    # here we have assumed it is the Django User model. It could be a Team, Company model too.
    # note that it needs to have an email field.
    used_id = request.user.id

    # example of how to insert the SUBSCRIBER_CUSTOMER_KEY: id in the metadata
    # to add customer.subscriber to the newly created/updated customer.
    metadata = {
        f"{djstripe_settings.djstripe_settings.SUBSCRIBER_CUSTOMER_KEY}": used_id,
        "user_id": used_id,
        "plan_id": plan.id,
    }

    try:
        # retreive the Stripe Customer.
        customer = djstripe_models.Customer.objects.get(subscriber=request.user)
        # Customer Object in DB.

        # ! Note that Stripe will always create a new Customer Object if customer id not provided
        # ! even if customer_email is provided!
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=customer.id,
            # payment_method_types=["bacs_debit"],  # for bacs_debit
            payment_intent_data={
                "setup_future_usage": "off_session",
                # so that the metadata gets copied to the associated Payment Intent and Charge Objects
                "metadata": metadata,
            },
            line_items=[
                {
                    "price_data": {
                        "currency": plan.price.currency,
                        # "currency": "gbp",  # for bacs_debit
                        "unit_amount": int(plan.price.amount * 100),
                        "product_data": {"name": plan.name},
                        "product_data": {
                            "name": plan.name,
                            "description": plan.description,
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,
        )

    except djstripe_models.Customer.DoesNotExist:  # "Customer Object not in DB.
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            # payment_method_types=["bacs_debit"],  # for bacs_debit
            payment_intent_data={
                "setup_future_usage": "off_session",
                # so that the metadata gets copied to the associated Payment Intent and Charge Objects
                "metadata": metadata,
            },
            line_items=[
                {
                    "price_data": {
                        "currency": plan.price.currency,
                        # "currency": "gbp",  # for bacs_debit
                        "unit_amount": int(plan.price.amount * 100),
                        "product_data": {"name": plan.name},
                        "product_data": {
                            "name": plan.name,
                            "description": plan.description,
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,
        )

    return session
