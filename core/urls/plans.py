from django.urls import path

from ..views.plans import checkout
from ..views.plans import payment_fail
from ..views.plans import payment_success
from ..views.plans import plan_detail
from ..views.plans import plan_list


urlpatterns = [
    # standard
    path("plans/", plan_list, name="plan_list"),
    path("plan/<int:id>/", plan_detail, name="plan_detail"),
    path("checkout/<int:id>/", checkout, name="plan_checkout"),
    path("payment-successed/", payment_success, name="payment_successed"),
    path("payment-failed/", payment_fail, name="payment_failed"),
]
