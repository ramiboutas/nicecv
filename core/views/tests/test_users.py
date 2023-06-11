from http import HTTPStatus

from django.urls import reverse

from config.test import TestCase


class CustomUserTests(TestCase):
    def test_signup(self):
        url = reverse("account_signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
