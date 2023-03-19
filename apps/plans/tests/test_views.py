from http import HTTPStatus

import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse
from django.test import TestCase

from apps.plans import views
from apps.plans.factories import PremiumPlanFactory


@pytest.mark.django_db
def test_plan_list_view(rf):
    request = rf.get(reverse("plans:list"))
    response = views.plan_list_view(request)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_plan_detail_view(rf, django_user_model):
    user = django_user_model.objects.create_user(
        username="username", password="password"
    )
    plan = PremiumPlanFactory()
    request = rf.get(plan.detail_url)
    request.user = user
    response = views.plan_detail_view(request, plan.id)
    assert response.status_code == HTTPStatus.OK
