from ..factories import UserFactory
from ..models import CustomUser
from config.test import TestCase


class UserFactoryTests(TestCase):
    def test_default_user_factory(self):
        user = UserFactory()
        self.assertEqual(user.username, UserFactory.username)
        self.assertEqual(user.password, UserFactory.password)
        self.assertEqual(user.email, UserFactory.email)

    def test_model_instance(self):
        user = CustomUser.objects.get(pk=UserFactory().pk)
        self.assertEqual(user.username, UserFactory.username)
