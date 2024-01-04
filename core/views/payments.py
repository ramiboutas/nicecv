import stripe
from django.db.models import Model
from django.urls import reverse
from django.conf import settings


from djstripe import models as djstripe_models
from djstripe import settings as djstripe_settings
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money

from ..templatetags.plan_pricing import get_plan_price


stripe.api_key = settings.STRIPE_SECRET_KEY

# https://stripe.com/docs/currencies?presentment-currency=DE#presentment-currencies
# Currencies marked with * are not supported by American Express
STANDARD_CURRENCIES = (
    "USD",
    "AED",
    # "AFN*",
    "ALL",
    "AMD",
    "ANG",
    # "AOA*",
    # "ARS*",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BIF",
    "BMD",
    "BND",
    # "BOB*",
    # "BRL*",
    "BSD",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHF",
    "CLP*",
    "CNY",
    "COP*",
    "CRC*",
    "CVE*",
    "CZK",
    "DJF*",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ETB",
    "EUR",
    "FJD",
    # "FKP*",
    "GBP",
    "GEL",
    "GIP",
    "GMD",
    "GNF*",
    "GTQ*",
    "GYD",
    "HKD",
    # "HNL*",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "ISK",
    "JMD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KRW",
    "KYD",
    "KZT",
    # "LAK*",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    # "MUR*",
    "MVR",
    "MWK",
    "MXN",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    # "NIO*",
    "NOK",
    "NPR",
    "NZD",
    "PAB*",
    # "PEN*",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    # "PYG*",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SEK",
    "SGD",
    # "SHP*",
    "SLE",
    "SOS",
    # "SRD*",
    # "STD*",
    "SZL",
    "THB",
    "TJS",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    # "UYU*",
    "UZS",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XCD",
    # "XOF*",
    # "XPF*",
    "YER",
    "ZAR",
    "ZMW",
)
# https://stripe.com/docs/currencies?presentment-currency=DE#zero-decimal
ZERO_DECIMAL_CURRENCIES = (
    "BIF",
    "CLP",
    "DJF",
    "GNF",
    "JPY",
    "KMF",
    "KRW",
    "MGA",
    "PYG",
    "RWF",
    "UGX",
    "VND",
    "VUV",
    "XAF",
    "XOF",
    "XPF",
)

# https://stripe.com/docs/currencies?presentment-currency=DE#three-decimal

THREE_DECIMAL_CURRENCIES = ("BHD", "JOD", "KWD", "OMR", "TND")


def round5(x):
    return 5 * round(x / 5)


def get_currency_and_amount(money: Money):
    if money.currency in STANDARD_CURRENCIES:
        return money.currency, int(100 * money.amount)
    elif money.currency in ZERO_DECIMAL_CURRENCIES:
        return money.currency, int(money.amount)
    elif money.currency in THREE_DECIMAL_CURRENCIES:
        return money.currency, round5(int(money.amount))
    else:
        return ("EUR", int(100 * convert_money(money, "EUR").amount))


def create_stripe_session(request, plan: Model):
    """
    Creates and returns a Stripe Checkout Session
    """

    money = get_plan_price(request, plan)
    currency, amount = get_currency_and_amount(money)

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

    return session
