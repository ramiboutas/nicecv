import pytest
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.factories import UserFactory
from plans.factories import PlanFactory
from plans.models import Order
from plans.models import Plan


@pytest.mark.django_db
class PlanTests(TestCase):
    def test_plan_instance(self):
        plan = Plan.objects.create(months=1, price=7)
        assert plan.months == 1
        assert str(plan) == "1 months"

    def test_one_single_month_value_is_allowed(self):
        Plan.objects.create(months=1, price=7)
        with pytest.raises(IntegrityError):
            Plan.objects.create(months=1, price=14)


@pytest.mark.django_db
class OrderTests(TestCase):
    def test_order_instance(self):
        user = UserFactory()
        plan = PlanFactory()
        order = Order.objects.create(user=user, plan=plan)
        assert order.user == user
        assert order.plan == plan
        assert str(order) == f"{order.created} - {user.email}"
