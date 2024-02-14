import stripe
from django.db.models import Model
from django.urls import reverse
from django.conf import settings


from djstripe import models as djstripe_models
from djstripe import settings as djstripe_settings


from ..templatetags.plan_pricing import get_currency_and_amount_for_stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(request, plan: Model):
    """
    Creates and returns a Stripe Checkout Session
    """

    currency, amount = get_currency_and_amount_for_stripe(request, plan)

    success_url = (
        request.build_absolute_uri(reverse("payment_successed"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )

    cancel_url = request.build_absolute_uri(
        reverse("payment_failed") + "?session_id={CHECKOUT_SESSION_ID}"
    )

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
        session = stripe.checkout.Session.create(  # pragma: no cover
            # payment_method_types=["card"],
            customer=customer.id,
            payment_intent_data={
                "setup_future_usage": "off_session",
                # so that the metadata gets copied to the associated Payment Intent and Charge Objects
                "metadata": metadata,
            },
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        # "currency": "gbp",  # for bacs_debit
                        "unit_amount": amount,
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
            # payment_method_types=["card"],
            payment_intent_data={
                "setup_future_usage": "off_session",
                # so that the metadata gets copied to the associated Payment Intent and Charge Objects
                "metadata": metadata,
            },
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
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
