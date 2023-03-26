from functools import cache
import sys
import inspect
import warnings

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

from . import models


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


def set_hidden_fields(form, fields: list):
    for field_name in fields:
        try:
            form.fields[field_name].widget = forms.HiddenInput()
        except KeyError:
            warnings.warn(f"{field_name} not found in {form.__class__.__name__}")


def update_widget_attrs(form, widget_attrs: dict, fields: list = None, id_prefix=""):
    field_list = form.fields if fields is None else fields
    prefix = "" if id_prefix == "" else f"{id_prefix}_"

    for field_name in field_list:
        new_widget_attrs = widget_attrs | {"id": f"id_{prefix}{field_name}"}
        try:
            form.fields[field_name].widget.attrs.update(new_widget_attrs)
        except KeyError:
            warnings.warn(f"{field_name} not found in {form.__class__.__name__}")


def create_chilform_widgets(form_obj, *args, **kwargs):
    # Getting instance for building a post url
    instance = kwargs.get("instance", None)
    # Building the widgets
    widget_attrs = build_widget_attrs(
        html_class="border-1 rounded-md hover:bg-slate-100 placeholder:italic border-slate-100",
        x_bind_class="active ? 'border-slate-500' : 'border-slate-100'",
        hx_post=instance.update_form_url() if instance is not None else "",
        hx_trigger="keyup changed delay:2s",
    )
    update_widget_attrs(form_obj, widget_attrs)
    set_hidden_fields(form_obj, ["profile"])


def create_settingform_widgets(form_obj, *args, **kwargs):
    set_hidden_fields(form_obj, ["profile"])
    for field_name in form_obj.fields:
        if field_name.startswith("active_"):
            checkbox_attrs = build_widget_attrs(
                html_class="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-600",
            )
            update_widget_attrs(form_obj, checkbox_attrs, fields=[field_name])
        elif field_name.startswith("label_"):
            textinput_attrs = build_widget_attrs(
                html_class="""block w-full rounded-md  py-1.5 border-slate-100
            text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300
            placeholder:text-gray-400 focus:ring-2 focus:ring-inset
            focus:ring-indigo-600 sm:text-sm sm:leading-6""",
                x_bind_class="active ? 'border-slate-500' : 'border-slate-100'",
            )
            update_widget_attrs(form_obj, textinput_attrs, fields=[field_name])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["public"]


class AbstractChildForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        create_chilform_widgets(self, *args, **kwargs)

    class Meta:
        fields = "__all__"


class FullnameForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Fullname


class JobtitleForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Jobtitle


class LocationForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Location


class BirthForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Birth


class PhoneForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Phone


class EmailForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Email


class WebsiteForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Website


class DescriptionForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Description


class SkillForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Skill


class SettingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        create_settingform_widgets(self, *args, **kwargs)

    class Meta(forms.ModelForm):
        fields = "__all__"
        model = models.ProfileSetting


@cache
def get_profile_child_modelforms() -> dict:
    """Returns a dict with model classes and form classes asociated with Profile model"""

    class_objs = {
        cls_obj.Meta.model: cls_obj
        for _, cls_obj in inspect.getmembers(sys.modules[__name__])
        if (inspect.isclass(cls_obj) and (AbstractChildForm in cls_obj.__bases__))
    }

    return class_objs


@cache
def get_child_modelform(Klass):
    """Returns the ModelForm associated with a Child Model"""
    ChildModel = getattr(models, Klass) if isinstance(Klass, str) else Klass

    if models.AbstractChild in ChildModel.__bases__:
        modelforms = get_profile_child_modelforms()
        return ChildModel, modelforms[ChildModel]
