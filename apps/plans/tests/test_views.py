from http import HTTPStatus

from django.urls import reverse
from config.test import TestCase
from django.test import RequestFactory


from apps.accounts.factories import UserFactory
from apps.plans.factories import PremiumPlanFactory
from apps.plans import views


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
