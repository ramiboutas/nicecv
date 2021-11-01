from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.standard_user = User.objects.create(username='myuser', email='myuser@email.com', password='myuserpass123')
        self.super_user = User.objects.create_superuser(username='superuser', email='superuser@email.com', password='superuserpass123')

    def test_standard_user(self):
        self.assertEqual(self.standard_user.username, 'myuser')
        self.assertEqual(self.standard_user.email, 'myuser@email.com')
        self.assertEqual(self.standard_user.password, 'myuserpass123')
        self.assertTrue(self.standard_user.is_active)
        self.assertFalse(self.standard_user.is_staff)
        self.assertFalse(self.standard_user.is_superuser)

    def test_super_user(self):
        self.assertEqual(self.super_user.username, 'superuser')
        self.assertEqual(self.super_user.email, 'superuser@email.com')
        self.assertTrue(self.super_user.is_active)
        self.assertTrue(self.super_user.is_staff)
        self.assertTrue(self.super_user.is_superuser)
