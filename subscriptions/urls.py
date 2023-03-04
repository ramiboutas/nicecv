from django.urls import path

from .views import hx_get_payment_methods_view
from .views import hx_update_price_view
from .views import payment_failed_view
from .views import payment_success_view
from .views import plan_list
from .views import proceed_with_payment_view
from .views import stripe_checkout_view
from .views import stripe_webhook_view


urlpatterns = [
    # standard
    path("", plan_list, name="subscriptions_plans"),
    path(
        "proceed-with-payment/",
        proceed_with_payment_view,
        name="payments_proceed_with_checkout",
    ),
    path("stripe/", stripe_checkout_view, name="payments_stripe_checkout"),
    path("stripe/webhook/", stripe_webhook_view, name="payments_stripe_webhook"),
    path("success/", payment_success_view, name="payments_success"),
    path("failed/", payment_failed_view, name="payments_failed"),
    # htmx urls
    path("hx/update-price/", hx_update_price_view, name="pricing_update_price"),
    path(
        "hx/get-payment-methods/",
        hx_get_payment_methods_view,
        name="pricing_get_payment_methods",
    ),
]
