import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.plans.factories import PlanFAQFactory
from apps.plans.factories import PremiumPlanFactory
from apps.plans.models import PremiumPlan
from apps.plans.models import FreePlan


@pytest.mark.django_db
class PremiumPlanTests(TestCase):
    def test_plan_instance(self):
        plan = PremiumPlan.objects.create(months=1, price=7)
        assert plan.months == 1
        assert str(plan) == "1 months"

    def test_one_single_month_value_is_allowed(self):
        PremiumPlan.objects.create(months=1, price=7)
        with pytest.raises(IntegrityError):
            PremiumPlan.objects.create(months=1, price=14)

    def test_plan_urls(self):
        plan = PremiumPlanFactory()
        assert plan.detail_url == reverse("plans:detail", kwargs={"id": plan.id})
        assert plan.checkout_url == reverse("plans:checkout", kwargs={"id": plan.id})


@pytest.mark.django_db
class FreePlanTests(TestCase):
    def test_one_instance_is_allowed(self):
        plan = FreePlan.get()
        with pytest.raises((IntegrityError, ValidationError)):
            FreePlan.objects.create(
                name="Free Plan 2", description="Description of free plan 2"
            )

    def test_when_instance_does_not_exist(self):
        plan = FreePlan.get()
        assert plan.name == "Free Plan"


@pytest.mark.django_db
class PlanFAQTest(TestCase):
    def test_planfaq_instance(self):
        faq = PlanFAQFactory()
        assert "?" in faq.question
        assert str(faq)
