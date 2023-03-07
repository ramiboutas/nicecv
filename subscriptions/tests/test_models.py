import pytest

from django.test import TestCase
from django.test import RequestFactory
from django.db.utils import IntegrityError

from subscriptions.models import Plan
from subscriptions.models import Order
from subscriptions.factories import PlanFactory
from accounts.factories import UserFactory

@pytest.mark.django_db
class PlanTests(TestCase):

    def test_plan_instance(self):
        plan = Plan.objects.create(months=1, price=7, saving=2)
        assert plan.months == 1
        assert str(plan) == '1 months'
    
    def test_one_default_plan_is_allowed(self):
        Plan.objects.create(months=1, price=7, saving=2, default=True)
        with pytest.raises(IntegrityError):
            Plan.objects.create(months=2, price=14, saving=4, default=True)

    def test_one_single_month_value_is_allowed(self):
        Plan.objects.create(months=1, price=7, saving=2, default=True)
        with pytest.raises(IntegrityError):
            Plan.objects.create(months=1, price=14, saving=4, default=True)


@pytest.mark.django_db
class OrderTests(TestCase):

    def test_order_instance(self):
        user = UserFactory()
        plan = PlanFactory()
        order = Order.objects.create(user=user, plan=plan)
        assert order.user == user
        assert order.plan == plan
        assert str(order) == f"{order.created} - {user.email}"

        
