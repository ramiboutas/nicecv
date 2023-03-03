import pytest

from django.test import TestCase
from django.urls import reverse



class CustomUserTests(TestCase):
    def test_signup(self):
        url = reverse("account_signup")
        response = self.client.get(url)
        assert response.status_code == 200
    