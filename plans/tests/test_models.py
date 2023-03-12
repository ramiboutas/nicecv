import pytest
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.factories import UserFactory
from plans.factories import PlanFactory
from plans.factories import PlanFAQFactory
from plans.models import Order
from plans.models import PremiumPlan


@pytest.mark.django_db
class PlanTests(TestCase):
    def test_plan_instance(self):
        plan = PremiumPlan.objects.create(months=1, price=7)
        assert plan.months == 1
        assert str(plan) == "1 months"

    def test_one_single_month_value_is_allowed(self):
        PremiumPlan.objects.create(months=1, price=7)
        with pytest.raises(IntegrityError):
            PremiumPlan.objects.create(months=1, price=14)

    def test_plan_checkout_url(self):
        plan = PlanFactory()
        assert plan.detail_url


@pytest.mark.django_db
class PlanFAQTest(TestCase):
    def test_planfaq_instance(self):
        faq = PlanFAQFactory()
        assert "?" in faq.question
        assert str(faq)


@pytest.mark.django_db
class OrderTests(TestCase):
    def test_order_instance(self):
        user = UserFactory()
        plan = PlanFactory()
        order = Order.objects.create(user=user, plan=plan)
        assert order.user == user
        assert order.plan == plan
        assert str(order) == f"{order.created} - {user.email}"
