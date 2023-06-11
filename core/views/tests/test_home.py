from http import HTTPStatus

from django.test import RequestFactory
from django.urls import resolve

from ..views import HomeView
from core.factories.users import UserFactory
from config.test import TestCase


class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_home_view_resolve(self):
        self.assertEqual(resolve("/").func.__name__, HomeView.as_view().__name__)

    def test_home_view_logged_in(self):
        request_factory = RequestFactory()
        request = request_factory.get("/")
        request.user = UserFactory()
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)
