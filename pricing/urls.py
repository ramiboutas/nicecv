from django.urls import path

from .views import PricingView, OrderView

urlpatterns = [
    path('', PricingView.as_view(), name='pricing'),
    path('', OrderView.as_view(), name='order_plan'),

]
