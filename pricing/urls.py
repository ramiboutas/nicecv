from django.urls import path

from .views import pricing_view
from . import hx_views

urlpatterns = [
    path('', pricing_view, name='pricing'),

]


hx_urlpatterns = [
    path('update-price/', hx_views.update_price, name='pricing_update_price'),
]



urlpatterns += hx_urlpatterns
