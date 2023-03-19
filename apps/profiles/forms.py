from django.forms import ModelForm

from .models import Profile


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["fullname", "email", "user"]


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
