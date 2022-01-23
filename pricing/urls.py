from django.urls import path

from .views import (pricing_view, get_payment_methods_view, update_price_view, get_payment_methods_view)

urlpatterns = [
    # standard
    path('', pricing_view, name='pricing_main'),
    # this is used when the user is not logged in so we redirect him to login
    # path('get-payment-methods/', get_payment_methods_view ,name='pricing_get_payment_methods'),


    # htmx urls
    path('hx/update-price/', update_price_view, name='pricing_update_price'),
    path('hx/get-payment-methods/', get_payment_methods_view ,name='pricing_get_payment_methods'),
]
