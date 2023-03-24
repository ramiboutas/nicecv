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

from .models import Description


def _build_text_input_attrs(instance=None):
    more_attrs = {}
    base_attrs = {
        "hx-trigger": "keyup changed delay:2s",
        "class": "border-1 rounded-md hover:bg-slate-100 placeholder:italic",
        ":class": mark_safe("active ? 'border-slate-500' : 'border-slate-100'"),
    }

    if instance is not None:
        more_attrs = more_attrs | {
            "hx-post": mark_safe(instance.update_form_url()),
        }

    return base_attrs | more_attrs


def _assign_hidden_to_fields(form, fields: list):
    for field in fields:
        form.fields[field].widget = forms.HiddenInput()


def build_single_child_input_widgets(form_obj, *args, **kwargs):
    instance = kwargs.get("instance", None)
    widget_attrs = _build_text_input_attrs(instance)
    form_obj.fields["text"].widget.attrs.update(widget_attrs)
    _assign_hidden_to_fields(form_obj, ["active", "profile"])


def build_description_input_widgets(form_obj, *args, **kwargs):
    instance = kwargs.get("instance", None)
    widget_attrs = _build_text_input_attrs(instance)
    form_obj.fields["label"].widget.attrs.update(widget_attrs)
    form_obj.fields["text"].widget.attrs.update(widget_attrs)
    _assign_hidden_to_fields(form_obj, ["active", "profile"])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]


class SimpleChildForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_single_child_input_widgets(self, *args, **kwargs)


class FullnameForm(SimpleChildForm):
    class Meta:
        model = Fullname
        fields = ["text", "active", "profile"]


class JobtitleForm(SimpleChildForm):
    class Meta:
        model = Jobtitle
        fields = ["text", "active", "profile"]


class LocationForm(SimpleChildForm):
    class Meta:
        model = Location
        fields = ["text", "active", "profile"]


class BirthForm(SimpleChildForm):
    class Meta:
        model = Birth
        fields = ["text", "active", "profile"]


class PhoneForm(SimpleChildForm):
    class Meta:
        model = Phone
        fields = ["text", "active", "profile"]


class EmailForm(SimpleChildForm):
    class Meta:
        model = Email
        fields = ["text", "active", "profile"]


class WebsiteForm(SimpleChildForm):
    class Meta:
        model = Website
        fields = ["text", "active", "profile"]


class DescriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_description_input_widgets(self, *args, **kwargs)

    class Meta:
        model = Description
        fields = "__all__"
