import datetime

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()
today = datetime.date.today()
delta_month = datetime.timedelta(days=30)


def create_user(user="user", email="user@email.com", password="userpass123"):
    return User.objects.create(
        username=user,
        email=email,
        password=password,
    )


def create_superuser(
    user="superuser", email="superuser@email.com", password="superuserpass12"
):
    return User.objects.create_superuser(
        username=user,
        email=email,
        password=password,
    )


class CustomUserTests(TestCase):
    @pytest.mark.django_db
    def test_standard_user(self):
        user = create_user()
        assert user.username == "user"
        assert user.email == "user@email.com"
        assert user.password, "myuserpass123"
        assert user.is_active == True
        assert user.is_staff == False
        assert user.is_superuser == False

    @pytest.mark.django_db
    def test_superuser(self):
        superuser = create_superuser()
        assert superuser.username == "superuser"
        assert superuser.email == "superuser@email.com"
        assert superuser.password, "superuserpass123"
        assert superuser.is_active == True
        assert superuser.is_staff == True

    @pytest.mark.django_db
    def test_has_premium_with_user_just_created(self):
        user = create_user()
        assert user.has_premium() == False

    @pytest.mark.django_db
    def test_has_premium_with_paid_until_none(self):
        user = create_user()
        user.paid_until = None
        user.save()
        assert user.has_premium() == False

    @pytest.mark.django_db
    def test_has_premium_with_paid_until_today(self):
        user = create_user()
        user.paid_until = today
        user.save()
        assert user.has_premium() == True

    @pytest.mark.django_db
    def test_has_premium_with_paid_until_expired(self):
        user = create_user()
        user.paid_until = today - delta_month
        user.save()
        assert user.has_premium() == False

    @pytest.mark.django_db
    def test_has_premium_with_plan(self):
        user = create_user()
        user.paid_until = today + delta_month
        user.save()
        assert user.has_premium() == True

    def test_set_paid_until_with_user_just_created(self):
        user = create_user()
        paid_months = 2
        user.set_paid_until(months=paid_months)
        assert user.has_premium() == True
        assert user.paid_until == today + datetime.timedelta(
            days=(365.25 / 12) * paid_months
        )

    def test_set_paid_until_with_paid_until_in_the_past(self):
        user = create_user()
        user.paid_until = today - delta_month
        paid_months = 2
        user.set_paid_until(months=paid_months)
        assert user.paid_until == today + datetime.timedelta(
            days=(365.25 / 12) * paid_months
        )

    def test_set_paid_until_with_paid_until_today(self):
        user = create_user()
        user.paid_until = today
        paid_months = 2
        user.set_paid_until(months=paid_months)
        assert user.paid_until == today + datetime.timedelta(
            days=(365.25 / 12) * paid_months
        )

    def test_set_paid_until_with_paid_until_in_the_future(self):
        user = create_user()
        user.paid_until = today + delta_month
        paid_months = 2
        user.set_paid_until(months=paid_months)
        assert user.paid_until == today + delta_month + datetime.timedelta(
            days=(365.25 / 12) * paid_months
        )
