from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from ..models.users import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )
