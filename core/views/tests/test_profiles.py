from django.test import RequestFactory
from django.urls import reverse
from profiles import _create_initial_profile

from config.test import TestCase
from core.factories.users import UserFactory
from core.sessions import get_or_create_session


class ProfileUtilsTests(TestCase):
    def test_initial_profile_with_guest_user(self):
        request = RequestFactory().get(reverse("profile_create"))
        request.session = {}
        session, request = get_or_create_session(request)
        profile, request = _create_initial_profile(request)

        assert profile.session == session
        assert profile.user is None

    def test_initial_profile_with_logged_in_user(self):
        request = RequestFactory().get(reverse("profile_create"))
        test_user = UserFactory()
        request.user = test_user
        profile, request = _create_initial_profile(request)
        assert profile.user == test_user
        assert profile.session is None
