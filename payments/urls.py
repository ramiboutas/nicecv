from django.urls import path

from .views import (proceed_with_payment_view, stripe_checkout_view, paypal_checkout_view, coinbase_checkout_view, payment_success_view, payment_failed_view, stripe_webhook_view)

urlpatterns = [
    path('proceed-with-payment/', proceed_with_payment_view ,name='payments_proceed_with_checkout'),
    path('stripe/', stripe_checkout_view, name='payments_stripe_checkout'),
    path('stripe/webhook/', stripe_webhook_view, name='payments_stripe_webhook'),
    path('paypal/', paypal_checkout_view, name='payments_paypal_checkout'),
    path('coinbase/', coinbase_checkout_view, name='payments_coinbase_checkout'),
    path('success/', payment_success_view, name='payments_success'),
    path('failed/', payment_failed_view, name='payments_failed'),

]
