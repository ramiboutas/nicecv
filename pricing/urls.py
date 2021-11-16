from django.urls import path

from .views import pricing_view, checkout_view, payment_view
from . import hx_views

urlpatterns = [
    path('', pricing_view, name='pricing'),
    path('checkout/', checkout_view, name='pricing_checkout'),
    path('procced-with-payment/', payment_view, name='procced_with_payment'),

]


hx_urlpatterns = [
    path('update-price/', hx_views.update_price, name='pricing_update_price'),
]



urlpatterns += hx_urlpatterns
