from http import HTTPStatus

from plans import plan_detail_view
from ...factories.plans import PremiumPlanFactory
from django.test import RequestFactory
from django.urls import reverse

from config.test import TestCase
from core.factories.users import UserFactory


class PlanViewTest(TestCase):
    def test_plan_list_view(self):
        response = self.client.get(reverse("plans:list"))
        assert response.status_code == HTTPStatus.OK

    def test_plan_detail_view(self):
        plan = PremiumPlanFactory()
        request = RequestFactory().get(plan.checkout_url)
        request.user = UserFactory()
        response = plan_detail_view(request, plan.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)
