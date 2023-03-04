from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve

from ..views import HomeView


class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get("/")
        assert response.status_code == HTTPStatus.OK

    def test_home_view_resolve(self):
        assert resolve("/").func.__name__ == HomeView.as_view().__name__
