import datetime
import pytest

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class CustomUserTests(TestCase):

    @pytest.mark.django_db
    def test_standard_user(self):
        user = User.objects.create(
            username="user",
            email="user@email.com",
            password="userpass123"
        )
        assert user.username == "user"
        assert user.email == "user@email.com"
        assert user.password, "myuserpass123"
        assert user.is_active == True
        assert user.is_staff == False
        assert user.is_superuser == False
    
    @pytest.mark.django_db
    def test_superuser(self):
        superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@email.com",
            password="superuserpass123",
        )
        assert superuser.username == "superuser"
        assert superuser.email == "superuser@email.com"
        assert superuser.password, "superuserpass123"
        assert superuser.is_active == True
        assert superuser.is_staff == True
        
    @pytest.mark.django_db
    def test_if_user_has_paid(self):
        today = datetime.date.today()
        delta_month = datetime.timedelta(days=30)
        user = User.objects.create(username="user", email="user@email.com", password="userpass123")
        # if user is just created
        assert user.has_premium() == False
        # user who has paid until today
        user.paid_until = today
        user.save()
        assert user.has_premium() == True
        # user with expired plan
        user.paid_until = today - delta_month
        user.save()
        assert user.has_premium() == False
        # user with paid plan
        user.paid_until = today + delta_month
        user.save()
        assert user.has_premium() == True
        # adding X months using the method set_paid_until
        paid_months = 2
        user.set_paid_until(months=paid_months)
        assert user.has_premium() == True
        assert user.paid_until == today + delta_month + datetime.timedelta(days=(365.25/12)*paid_months)


