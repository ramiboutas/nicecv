from http import HTTPStatus

from config.test import TestCase
from django.urls import reverse


class CustomUserTests(TestCase):
    def test_signup(self):
        url = reverse("account_signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
