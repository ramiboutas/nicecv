from django.urls import path

from .views import payment_failed_view
from .views import payment_success_view
from .views import paypal_checkout_view
from .views import plan_list
from .views import stripe_checkout_view
from .views import stripe_webhook_view

app_name = "plans"

urlpatterns = [
    # standard
    path("", plan_list, name="list"),
    path("stripe/", stripe_checkout_view, name="stripe_checkout"),
    path("paypal/", paypal_checkout_view, name="paypal_checkout"),
    path("stripe/webhook/", stripe_webhook_view, name="stripe_webhook"),
    path("payment-success/", payment_success_view, name="payment_success"),
    path("payment-failed/", payment_failed_view, name="payment_failed"),
]
