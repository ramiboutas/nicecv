import datetime

import pytest
from django.test import TestCase

from accounts.factories import SuperUserFactory
from accounts.factories import UserFactory
from plans.factories import PlanFactory

today = datetime.date.today()
delta_month = datetime.timedelta(days=30)


@pytest.mark.django_db
class CustomUserTests(TestCase):
    def test_standard_user(self):
        user = UserFactory()
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_superuser(self):
        superuser = SuperUserFactory()
        assert superuser.is_active
        assert superuser.is_staff

    def test_has_premium_with_user_just_created(self):
        user = UserFactory()
        assert not user.has_active_plan()

    def test_has_premium_with_paid_until_none(self):
        user = UserFactory()
        user.paid_until = None
        user.save()
        assert not user.has_active_plan()

    def test_has_premium_with_paid_until_today(self):
        user = UserFactory()
        user.paid_until = today
        user.save()
        assert user.has_active_plan()

    def test_has_premium_with_paid_until_expired(self):
        user = UserFactory()
        user.paid_until = today - delta_month
        user.save()
        assert not user.has_active_plan()

    def test_has_premium_with_plan(self):
        user = UserFactory()
        user.paid_until = today + delta_month
        user.save()
        assert user.has_active_plan()

    def test_set_paid_until_with_user_just_created(self):
        user = UserFactory()
        plan = PlanFactory()
        user.set_plan(plan=plan)
        assert user.has_active_plan()
        assert user.paid_until == today + datetime.timedelta(
            days=(365.25 / 12) * plan.months
        )

    def test_set_paid_until_with_paid_until_in_the_past(self):
        user = UserFactory()
        user.paid_until = today - delta_month
        plan = PlanFactory()
        user.set_plan(plan=plan)
        assert user.paid_until == today + datetime.timedelta(
            days=(365.25 / 12) * plan.months
        )

    def test_set_paid_until_with_paid_until_today(self):
        user = UserFactory()
        plan = PlanFactory()
        user.paid_until = today
        user.set_plan(plan=plan)
        assert user.paid_until == today + datetime.timedelta(
            days=(365.25 / 12) * plan.months
        )

    def test_set_paid_until_with_paid_until_in_the_future(self):
        user = UserFactory()
        user.paid_until = today + delta_month
        plan = PlanFactory()
        user.set_plan(plan=plan)
        assert user.paid_until == today + delta_month + datetime.timedelta(
            days=(365.25 / 12) * plan.months
        )
