from django import forms
from django.utils.safestring import mark_safe

from .models import Profile
from .models import Fullname
from .models import Jobtitle
from .models import Location
from .models import Birth
from .models import Phone
from .models import Email
from .models import Website


def _build_child_input_attrs(instance=None):
    more_attrs = {}
    base_attrs = {
        "hx-trigger": "keyup changed delay:1s",
        "class": "border-2 border-dashed rounded-md hover:bg-slate-100 placeholder:italic",
        ":class": mark_safe("active ? 'border-slate-500' : 'border-slate-200'"),
    }

    if instance is not None:
        more_attrs = more_attrs | {
            "hx-post": mark_safe(instance.update_form_url),
        }

    return base_attrs | more_attrs


def _manage_single_child_input_widgets(form_obj, *args, **kwargs):
    instance = kwargs.get("instance", None)
    widget_attrs = _build_child_input_attrs(instance)
    form_obj.fields["text"].widget.attrs.update(widget_attrs)
    form_obj.fields["active"].widget = forms.HiddenInput()
    form_obj.fields["profile"].widget = forms.HiddenInput()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]


class FullnameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _manage_single_child_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Fullname
        fields = ["text", "active", "profile"]


class JobtitleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _manage_single_child_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Jobtitle
        fields = ["text", "active", "profile"]


class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _manage_single_child_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Location
        fields = ["text", "active", "profile"]


class BirthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _manage_single_child_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Birth
        fields = ["text", "active", "profile"]


class PhoneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _manage_single_child_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Phone
        fields = ["text", "active", "profile"]


class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _manage_single_child_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Email
        fields = ["text", "active", "profile"]


class WebsiteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _manage_single_child_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Website
        fields = ["text", "active", "profile"]


class FieldActivationForm:
    # TODO: Nested form if possible
    pass


def get_form_object(form: str):
    mappings = {
        "FullnameForm": FullnameForm,
        "ProfileForm": ProfileForm,
    }
    try:
        return mappings[form]
    except KeyError:
        pass
