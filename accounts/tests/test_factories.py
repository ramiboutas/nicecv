import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..factories import UserFactory
from ..models import CustomUser

class UserFactoryTests(TestCase):

    @pytest.mark.django_db
    def test_default_user_factory(self):
        user = UserFactory()

        assert user.username == UserFactory.username
        assert user.password == UserFactory.password
        assert user.email == UserFactory.email

    @pytest.mark.django_db
    def test_model_instance(self):
        user = CustomUser.objects.get(pk=UserFactory().pk)
        assert user.username == UserFactory.username

