import pytest

from django.urls import reverse

from ..utils import create_initial_profile
from ..models import Profile
from apps.accounts.factories import UserFactory


@pytest.mark.django_db
def test_initial_profile_with_logged_in_user(rf):
    request = rf.get(reverse("profiles:create"))
    request.user = UserFactory()
    profile, request = create_initial_profile(request)
    assert profile.user is not None
    assert profile.session is None


@pytest.mark.django_db
def test_initial_profile_with_guest_user(rf):
    request = rf.get(reverse("profiles:create"))
    profile, request = create_initial_profile(request)
    assert profile.user is not None
    assert profile.session is None
