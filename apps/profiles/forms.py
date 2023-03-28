from functools import cache
import sys
import inspect
import warnings

from django import forms
from django.utils.safestring import mark_safe

from apps.core.classes import get_child_models
from . import models
from .models import SingleItemChild


def build_widget_attrs(
    html_class=None,  # html class
    x_bind_class=None,  # alpinejs :class attr.
    hx_post=None,  # htmx hx-post method
    hx_trigger=None,  # htmx hx-trigger method
):
    attrs = {}
    if html_class:
        attrs = attrs | {"class": mark_safe(html_class)}
    if x_bind_class:
        attrs = attrs | {":class": mark_safe(x_bind_class)}
    if hx_post:
        attrs = attrs | {"hx-post": mark_safe(hx_post)}
    if hx_trigger:
        attrs = attrs | {"hx-trigger": mark_safe(hx_trigger)}

    return attrs


def set_hidden(form, fields: list):
    for field_name in fields:
        try:
            form.fields[field_name].widget = forms.HiddenInput()
        except KeyError:
            warnings.warn(f"{field_name} not found in {form.__class__.__name__}")


def set_widget_attrs(form, widget_attrs: dict, fields: list = None):
    field_list = form.fields if fields is None else fields
    for field_name in field_list:
        try:
            form.fields[field_name].widget.attrs.update(widget_attrs)
        except KeyError:
            warnings.warn(f"{field_name} not found in {form.__class__.__name__}")


def create_childform_widgets(form_obj, *args, **kwargs):
    # Getting instance for building a post url
    instance = kwargs.get("instance", None)
    # Building the widgets
    widget_attrs = build_widget_attrs(
        html_class="border-1 rounded-md hover:bg-slate-100 placeholder:italic border-slate-100",
        x_bind_class="active ? 'border-slate-500' : 'border-slate-100'",
        hx_post=instance.update_form_url() if instance is not None else "",
        hx_trigger="keyup changed delay:2s",
    )
    set_widget_attrs(form_obj, widget_attrs)
    set_hidden(form_obj, ["profile"])


def create_label_settingform_widgets(form_obj, *args, **kwargs):
    set_hidden(form_obj, ["profile"])
    for field_name in form_obj.fields:
        textinput_attrs = build_widget_attrs(
            html_class="""block w-full rounded-md  py-1.5 border-slate-100
        text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300
        placeholder:text-gray-400 focus:ring-2 focus:ring-inset
        focus:ring-indigo-600 sm:text-sm sm:leading-6""",
            x_bind_class="active ? 'border-indigo-500' : 'border-indigo-100'",
        )
        set_widget_attrs(form_obj, textinput_attrs, fields=[field_name])


def create_activation_settingform_widgets(form_obj, *args, **kwargs):
    set_hidden(form_obj, ["profile"])
    for field_name in form_obj.fields:
        bool_attrs = build_widget_attrs(
            html_class="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-600",
        )
        set_widget_attrs(form_obj, bool_attrs, fields=[field_name])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["public"]


class SingleItemChildForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        create_childform_widgets(self, *args, **kwargs)

    class Meta:
        fields = ["profile", "text"]


class FullnameForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Fullname


class JobtitleForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Jobtitle


class LocationForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Location


class BirthForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Birth


class PhoneForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Phone


class EmailForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Email


class WebsiteForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Website


class DescriptionForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = models.Description


class ProfileSettingsForm(forms.ModelForm):
    pass


class ActivationSettingsForm(ProfileSettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        create_activation_settingform_widgets(self, *args, **kwargs)

    class Meta(forms.ModelForm):
        fields = "__all__"
        model = models.ActivationSettings


class LabelSettingsForm(ProfileSettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        create_label_settingform_widgets(self, *args, **kwargs)

    class Meta(forms.ModelForm):
        fields = "__all__"
        model = models.LabelSettings


@cache
def get_profile_modelforms(settings=False, single_item=True) -> dict:
    """Returns a dict with model classes and form classes asociated with Profile model"""
    KlassDict = {}
    Forms = [k for _, k in inspect.getmembers(sys.modules[__name__], inspect.isclass)]

    for Form in Forms:
        if single_item and (SingleItemChildForm in Form.__bases__):
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
