from http import HTTPStatus

from django.test import RequestFactory
from django.test import TestCase
from django.urls import resolve
from django.urls import reverse

from ..views import HomeView
from apps.accounts.factories import UserFactory


class HomeViewTests(TestCase):
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


class ContactViewTests(TestCase):
    def test_contact_view(self):
        url = reverse("core:contact")
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
