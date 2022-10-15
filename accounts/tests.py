import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve


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

    def test_has_paid_no_setting_paid_until(self):
        self.assertFalse(self.standard_user.has_paid())

    def test_has_paid_past(self):
        self.standard_user.paid_until = datetime.date.today() - datetime.timedelta(days=30)
        self.standard_user.save()
        self.assertFalse(self.standard_user.has_paid())

    def test_has_paid_future(self):
        self.standard_user.paid_until = datetime.date.today() + datetime.timedelta(days=30)
        self.standard_user.save()
        self.assertTrue(self.standard_user.has_paid())

    def test_has_paid_today(self):
        self.standard_user.paid_until = datetime.date.today()
        self.standard_user.save()
        self.assertTrue(self.standard_user.has_paid())

    def test_set_paid_until_none(self):
        "the user has nothig ordered"
        self.standard_user.paid_until = None
        self.standard_user.save()
        self.standard_user.set_paid_until(months=1)
        self.standard_user.save()
        self.assertTrue(self.standard_user.has_paid())

    def test_set_paid_until_1_plus_1(self):
        "the user is already premium member but add one month more"
        self.standard_user.paid_until = datetime.date.today() + datetime.timedelta(days=365.25/12)
        self.standard_user.save()
        self.standard_user.set_paid_until(months=1)
        self.standard_user.save()
        self.assertEqual(self.standard_user.paid_until, datetime.date.today() + datetime.timedelta(days=2*365.25/12))


class SignupPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@gmail.com'
    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    # def test_signup_template(self):
    #     self.assertEqual(self.response.status_code, 200)
    #     self.assertTemplateUsed(self.response, 'account/signup.html')
    #     self.assertNotContains(self.response, 'Hi, this text is so random that should not be on your page :)')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
