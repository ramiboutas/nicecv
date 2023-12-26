import datetime

from ...factories.users import SuperUserFactory
from ...factories.users import UserFactory
from ...factories.users import UserPremiumPlanFactory
from ..plans import FreePlan
from ..plans import PremiumPlan
from config.test import TestCase


class UserTests(TestCase):
    def test_standard_user(self):
        user = UserFactory()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser(self):
        superuser = SuperUserFactory()
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)

    def test_user_just_created_with_free_plan(self):
        user = UserFactory()
        self.assertIsInstance(user.plan, FreePlan)

    def test_user_with_premium_plan(self):
        user_plan = UserPremiumPlanFactory()
        self.assertGreater(user_plan.expires, datetime.date.today())
        self.assertIsInstance(user_plan.plan, PremiumPlan)
        self.assertEqual(user_plan.user.plan, user_plan.plan)


class UserPremiumPlanTests(TestCase):
    def test_instance_str(self):
        user_plan = UserPremiumPlanFactory()
        self.assertIsNotNone(str(user_plan))
