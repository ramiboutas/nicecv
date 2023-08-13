from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from ..models.users import User
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            # "email",
            "username",
            "first_name",
            "last_name",
        )
