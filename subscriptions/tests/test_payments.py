import pytest

from django.test import TestCase

from ..payments import fulfill_order
from ..models import Order
from ..models import Plan




class FulfillOrderTests(TestCase):

    @pytest.mark.django_db
    def test_fulfill_order_with_user_id_none(self):
        ok = fulfill_order(user_id=None, plan_id=1)
        assert ok == False

    @pytest.mark.django_db
    def test_fulfill_order_with_plan_id_none(self):
        ok = fulfill_order(user_id=1, plan_id=None)
        assert ok == False
    
