from functools import cache
import sys
import inspect
import warnings

from django import forms
from django.utils.safestring import mark_safe

from . import models
from .models import Fullname
from .models import Jobtitle
from .models import Location
from .models import Birth
from .models import Phone
from .models import Email
from .models import Website
from .models import Description


TEXT_INPUT_CLASS = (
    "border-1 rounded-md hover:bg-slate-100 placeholder:italic border-slate-100"
)
TEXT_INPUT_XBIND_CLASS = "active ? 'border-slate-500' : 'border-slate-100'"
TEXT_INPUT_HX_TRIGGER = "keyup changed delay:2s"


def build_widget_attrs(html_class=None, x_class=None, hx_post=None, hx_trigger=None):
    attrs = {}

    if html_class:
        # html class
        attrs = attrs | {"class": mark_safe(html_class)}

    if x_class:
        # alpinejs :class attr.
        attrs = attrs | {":class": mark_safe(x_class)}

    if hx_post:
        # htmx hx-post method
        attrs = attrs | {"hx-post": mark_safe(hx_post)}

    if hx_trigger:
        # htmx hx-trigger method
        attrs = attrs | {"hx-trigger": mark_safe(hx_trigger)}

    return attrs


def set_widget_attrs(form, attrs: dict, fields: list = None):
    field_list = form.fields if fields is None else fields
    for field_name in field_list:
        try:
            form.fields[field_name].widget.attrs.update(attrs)
        except KeyError:
            warnings.warn(f"{field_name} not found in {form.__class__.__name__}")


def create_childform_widgets(form_obj, *args, **kwargs):
    instance = kwargs.get("instance", None)
    attrs = build_widget_attrs(
        html_class=TEXT_INPUT_CLASS,
        x_class=TEXT_INPUT_XBIND_CLASS,
        hx_post=instance.update_form_url() if instance is not None else "",
        hx_trigger=TEXT_INPUT_HX_TRIGGER,
    )
    set_widget_attrs(form_obj, attrs)


def create_label_settingform(form_obj, *args, **kwargs):
    for field_name in form_obj.fields:
        attrs = build_widget_attrs(
            html_class=TEXT_INPUT_CLASS, x_class=TEXT_INPUT_XBIND_CLASS
        )
        set_widget_attrs(form_obj, attrs, fields=[field_name])


def process_activation_settingform(form_obj, *args, **kwargs):
    for field_name in form_obj.fields:
        bool_attrs = build_widget_attrs(
            html_class="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-600",
        )
        set_widget_attrs(form_obj, bool_attrs, fields=[field_name])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["public"]


class SimpleChildForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        create_childform_widgets(self, *args, **kwargs)

    class Meta:
        fields = ["text"]


class FullnameForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Fullname


class JobtitleForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Jobtitle


class LocationForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Location


class BirthForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Birth


class PhoneForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Phone


class EmailForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Email


class WebsiteForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Website


class DescriptionForm(SimpleChildForm):
    class Meta(SimpleChildForm.Meta):
        model = Description


class ProfileSettingsForm(forms.ModelForm):
    pass


class ActivationSettingsForm(ProfileSettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        process_activation_settingform(self, *args, **kwargs)

    class Meta(forms.ModelForm):
        fields = "__all__"
        exclude = ["profile"]
        model = models.ActivationSettings


class LabelSettingsForm(ProfileSettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        create_label_settingform(self, *args, **kwargs)

    class Meta(forms.ModelForm):
        fields = "__all__"
        exclude = ["profile"]
        model = models.LabelSettings


@cache
def get_profile_modelforms(settings=False, single_item=True) -> dict:
    """Returns a dict with model classes and form classes asociated with Profile model"""
    KlassDict = {}
    Forms = [k for _, k in inspect.getmembers(sys.modules[__name__], inspect.isclass)]

    for Form in Forms:
        if single_item and (SimpleChildForm in Form.__bases__):
            KlassDict[Form.Meta.model] = Form
        if settings and (ProfileSettingsForm in Form.__bases__):
            KlassDict[Form.Meta.model] = Form

    return KlassDict


@cache
def get_modelform(Klass):
    """Returns the ModelForm associated with a Profile Model"""
    Model = getattr(models, Klass) if isinstance(Klass, str) else Klass
    modelforms = get_profile_modelforms(settings=True)
    return Model, modelforms[Model]
