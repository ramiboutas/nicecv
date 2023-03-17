from http import HTTPStatus

from django.test import RequestFactory
from django.test import TestCase
from django.urls import resolve

from ..views import HomeView
from apps.accounts.factories import UserFactory


class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get("/")
        assert response.status_code == HTTPStatus.OK

    def test_home_view_resolve(self):
        assert resolve("/").func.__name__ == HomeView.as_view().__name__

    def test_home_view_logged_in(self):
        # it should redirect to profile list view if user is logged in
        request_factory = RequestFactory()
        request = request_factory.get("/")
        request.user = UserFactory()
        response = HomeView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
