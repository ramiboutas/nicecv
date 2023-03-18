import datetime
import pytest
from django.test import TestCase

from apps.accounts.models import UserPremiumPlan
from apps.accounts.factories import SuperUserFactory
from apps.accounts.factories import UserFactory
from apps.accounts.factories import UserPremiumPlanFactory
from apps.plans.factories import PremiumPlanFactory
from apps.plans.models import FreePlan
from apps.plans.models import PremiumPlan


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

    @pytest.mark.django_db
    def test_user_with_premium_plan(self):
        user_plan = UserPremiumPlanFactory()
        assert user_plan.expires > datetime.date.today()


@pytest.mark.django_db
class UserPremiumPlanTests(TestCase):
    def test_instance_str(self):
        user_plan = UserPremiumPlanFactory()
        assert type(str(user_plan)) == str
