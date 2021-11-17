from django.urls import path

from .views import (pricing_view, get_payment_methods_view, proceed_with_payment_view, hx_update_price_view, hx_get_payment_methods_view)

urlpatterns = [
    # standard
    path('', pricing_view, name='pricing_main'),
    # this is used when the user is not logged in so we redirect him to login
    path('get-payment-methods/', get_payment_methods_view ,name='pricing_get_payment_methods'),
    path('proceed-with-payment/', proceed_with_payment_view ,name='pricing_proceed_with_payment'),

    # htmx urls
    path('hx/update-price/', hx_update_price_view, name='pricing_hx_update_price'),
    path('hx/get-payment-methods/', hx_get_payment_methods_view ,name='pricing_hx_get_payment_methods'),
]
