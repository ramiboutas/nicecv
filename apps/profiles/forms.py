from django.forms import ModelForm

from .models import Profile
from .models import Fullname


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["email", "user"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]


class FullnameTextForm(ModelForm):
    class Meta:
        model = Fullname
        fields = ["text"]


class FieldActivationForm:
    # TODO: Nested form if possible
    pass


def get_form_object(form: str):
    mappings = {
        "FullnameTextForm": FullnameTextForm,
        "ProfileForm": ProfileForm,
    }
    try:
        return mappings[form]
    except KeyError:
        pass
