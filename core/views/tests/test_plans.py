from http import HTTPStatus

from django.test import RequestFactory
from django.urls import reverse

from core.factories.users import UserFactory
from apps.plans import views
from apps.plans.factories import PremiumPlanFactory
from config.test import TestCase


class PlanViewTest(TestCase):
    def test_plan_list_view(self):
        response = self.client.get(reverse("plans:list"))
        assert response.status_code == HTTPStatus.OK

    def test_plan_detail_view(self):
        plan = PremiumPlanFactory()
        request = RequestFactory().get(plan.checkout_url)
        request.user = UserFactory()
        response = views.plan_detail_view(request, plan.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)
