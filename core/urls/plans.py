from django.urls import include
from django.urls import path

from ..views.plans import checkout
from ..views.plans import payment_fail
from ..views.plans import payment_success
from ..views.plans import plan_detail
from ..views.plans import plan_list
from ..views.plans import stripe_webhook

app_name = "plans"

urlpatterns = [
    # standard
    path("", plan_list, name="list"),
    path("<int:id>/", plan_detail, name="detail"),
    path("checkout/<int:id>/", checkout, name="checkout"),
    path("payment-successed/", payment_success, name="payment-successed"),
    path("payment-failed/", payment_fail, name="payment-failed"),
    path("webhook/", stripe_webhook, name="webhook-intent"),
]
