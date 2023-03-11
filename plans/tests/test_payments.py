import pytest
from django.test import RequestFactory
from django.test import TestCase

from accounts.factories import UserFactory
from plans.factories import PlanFactory
from plans.payments import create_stripe_session
from plans.payments import fulfill_order


@pytest.mark.django_db
class FulfillOrderTests(TestCase):
    def test_fulfill_order_with_user_id_none(self):
        ok = fulfill_order(user_id=None, plan_id=1)
        assert ok == False

    def test_fulfill_order_with_plan_id_none(self):
        ok = fulfill_order(user_id=1, plan_id=None)
        assert ok == False

    def test_fulfill_order_with_plan_id_and_user_id(self):
        user = UserFactory()
        plan = PlanFactory()
        ok = fulfill_order(user_id=user.id, plan_id=plan.id)
        assert ok == True

    def test_fulfill_order_with_user_that_does_not_exist(self):
        plan = PlanFactory()
        ok = fulfill_order(user_id=1000, plan_id=plan.id)
        assert ok == False

    def test_fulfill_order_with_plan_that_does_not_exist(self):
        user = UserFactory()
        ok = fulfill_order(user_id=user.id, plan_id=1000)
        assert ok == False


@pytest.mark.django_db
class StripeSessionTests(TestCase):
    @pytest.mark.slow
    def test_create_stripe_session(self):
        request_factory = RequestFactory()
        request = request_factory.get("/")
        request.user = UserFactory()
        session = create_stripe_session(request, plan=PlanFactory())
        assert ("checkout.stripe.com" in session["url"]) == True
