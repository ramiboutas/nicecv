from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.urls import reverse

from ...factories.plans import PremiumPlanFactory
from ..plans import FreePlan
from ..plans import PremiumPlan
from config.test import TestCase


class PremiumPlanTests(TestCase):
    def test_plan_instance(self):
        plan = PremiumPlan.objects.create(months=1, price=7)
        self.assertEqual(plan.months, 1)
        self.assertEqual(str(plan), "1 months")

    def test_one_single_month_value_is_allowed(self):
        PremiumPlan.objects.create(months=1, price=7)
        with self.assertRaises(IntegrityError):
            PremiumPlan.objects.create(months=1, price=14)

    def test_plan_urls(self):
        plan = PremiumPlanFactory()
        self.assertEqual(
            plan.detail_url, reverse("plan_detail", kwargs={"id": plan.id})
        )
        self.assertEqual(
            plan.checkout_url, reverse("plan_checkout", kwargs={"id": plan.id})
        )


class FreePlanTests(TestCase):
    def test_one_instance_is_allowed(self):
        FreePlan.get()
        with self.assertRaises((IntegrityError, ValidationError)):
            FreePlan.objects.create(name="Free Plan 2", description="Description")

    def test_when_instance_does_not_exist(self):
        plan = FreePlan.get()
        self.assertEqual(plan.name, "Free Plan")
