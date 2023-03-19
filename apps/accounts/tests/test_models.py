import datetime
import pytest
from django.test import TestCase

from apps.accounts.models import UserPremiumPlan
from apps.plans.models import FreePlan
from apps.plans.models import PremiumPlan

from apps.accounts.factories import SuperUserFactory
from apps.accounts.factories import UserFactory
from apps.accounts.factories import UserPremiumPlanFactory
from apps.plans.factories import PremiumPlanFactory


@pytest.mark.django_db(transaction=True)
class CustomUserTests(TestCase):
    @pytest.mark.django_db
    def test_standard_user(self):
        user = UserFactory()
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    @pytest.mark.django_db
    def test_superuser(self):
        superuser = SuperUserFactory()
        assert superuser.is_active
        assert superuser.is_staff

    @pytest.mark.django_db
    def test_user_just_created_with_free_plan(self):
        user = UserFactory()
        assert isinstance(user.get_actual_plan(), FreePlan)
        assert user.number_of_profiles == user.get_actual_plan().profiles

    @pytest.mark.django_db
    def test_user_with_premium_plan(self):
        user_plan = UserPremiumPlanFactory()
        assert user_plan.expires > datetime.date.today()
        assert isinstance(user_plan.plan, PremiumPlan)
        assert user_plan.user.get_actual_plan() == user_plan.plan
        assert user_plan.user.number_of_profiles == user_plan.plan.profiles


@pytest.mark.django_db
class UserPremiumPlanTests(TestCase):
    def test_instance_str(self):
        user_plan = UserPremiumPlanFactory()
        assert type(str(user_plan)) == str
