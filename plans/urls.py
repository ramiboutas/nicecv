from django.urls import path
from django.urls import include

from . import views

app_name = "plans"

urlpatterns = [
    # standard
    path("", views.plan_list, name="list"),
    path("<int:id>/", views.plan_detail_view, name="detail"),
    # path("stripe/<int:id>/", views.stripe_checkout_view, name="stripe-checkout"),
    # path("stripe/webhook/", views.stripe_webhook_view, name="stripe-webhook"),
    # path("payment-success/", views.payment_success_view, name="payment-success"),
    # path("payment-failed/", views.payment_failed_view, name="payment-failed"),
    # payment related urls
    path("checkout/<int:id>/", views.checkout_view, name="checkout"),
    path("success/", views.payment_success_view, name="success"),
    path("webhook/", views.stripe_webhook_view, name="webhook-intent"),
]
