from django.urls import include
from django.urls import path

from . import views

app_name = "plans"

urlpatterns = [
    # standard
    path("", views.plan_list_view, name="list"),
    path("<int:id>/", views.plan_detail_view, name="detail"),
    path("checkout/<int:id>/", views.checkout_view, name="checkout"),
    path("payment-successed/", views.payment_success_view, name="payment-successed"),
    path("payment-failed/", views.payment_fail_view, name="payment-failed"),
    path("webhook/", views.stripe_webhook_view, name="webhook-intent"),
]
