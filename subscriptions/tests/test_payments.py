import pytest
import factory

from django.test import TestCase

from subscriptions.payments import fulfill_order
from subscriptions.models import Order
from subscriptions.models import Plan
from subscriptions.factories import PlanFactory
from accounts.factories import UserFactory
 

class FulfillOrderTests(TestCase):
    # TODO: 
    # https://www.reddit.com/r/django/comments/loiu5x/django_pytest_database_access_not_allowed_error/
    # https://factoryboy.readthedocs.io/en/stable/#using-factories
    
    @pytest.fixtures.transactional_db
    def test_fulfill_order_with_user_id_none(self):
        ok = fulfill_order(user_id=None, plan_id=1)
        assert ok == False
    
    @pytest.fixtures.transactional_db
    def test_fulfill_order_with_plan_id_none(self):
        ok = fulfill_order(user_id=1, plan_id=None)
        assert ok == False
    
    @pytest.fixtures.transactional_db
    def test_fulfill_order_with_plan_id_and_user_id(self):
        user = factory.SubFactory(UserFactory)
        plan = factory.SubFactory(PlanFactory)
        ok = fulfill_order(user_id=user.id, plan_id=plan.id)
        assert ok == True
    
    @pytest.fixtures.transactional_db
    def test_fulfill_order_with_plan_id_does_not_exist(self):
        plan = factory.SubFactory(PlanFactory)
        ok = fulfill_order(user_id=2, plan_id=plan.id)
        assert ok == False
    
    @pytest.fixtures.transactional_db
    def test_fulfill_order_with_plan_id_does_not_exist(self):
        user = factory.SubFactory(UserFactory)
        ok = fulfill_order(user_id=user.id, plan_id=2)
        assert ok == False


with factory.debug():
    obj = FulfillOrderTests()


import logging
logger = logging.getLogger('factory')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)