from functools import cache
import sys
import inspect
import warnings

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

from . import models


def build_text_input_attrs(instance=None):
    more_attrs = {}
    base_attrs = {
        "hx-trigger": "keyup changed delay:2s",
        "class": "border-1 rounded-md hover:bg-slate-100 placeholder:italic",
        ":class": mark_safe("active ? 'border-slate-500' : 'border-slate-100'"),
    }

    if instance:
        more_attrs = more_attrs | {
            "hx-post": mark_safe(instance.update_form_url()),
        }

    return base_attrs | more_attrs


def set_hidden_fields(form, fields: list):
    for field in fields:
        try:
            form.fields[field].widget = forms.HiddenInput()
        except KeyError:
            if settings.DEBUG:
                warnings.warn(
                    f"{field} not found in the form {form.__class__.__name__}"
                )


def build_child_input_widgets(form_obj, *args, **kwargs):
    instance = kwargs.get("instance", None)
    widget_attrs = build_text_input_attrs(instance)
    for field_name in form_obj.fields:
        form_obj.fields[field_name].widget.attrs.update(widget_attrs)
    set_hidden_fields(form_obj, ["active", "profile", "label"])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = "__all__"
        exclude = ["user"]


class AbstractChildForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_child_input_widgets(self, *args, **kwargs)

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


class LabelForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Label


class DescriptionForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Description


class SkillForm(AbstractChildForm):
    class Meta(AbstractChildForm.Meta):
        model = models.Skill


@cache
def get_profile_child_modelforms() -> dict:
    """Returns a dict with model classes and form classes asociated with Profile model"""

    class_objs = {
        cls_obj.Meta.model: cls_obj
        for _, cls_obj in inspect.getmembers(sys.modules[__name__])
        if (inspect.isclass(cls_obj) and (AbstractChildForm in cls_obj.__bases__))
    }
    print(class_objs)

    return class_objs


@cache
def get_child_modelform(Klass):
    """Returns the ModelForm associated with a Child Model"""
    ChildModel = getattr(models, Klass) if isinstance(Klass, str) else Klass

    if models.AbstractChild in ChildModel.__bases__:
        modelforms = get_profile_child_modelforms()
        return ChildModel, modelforms[ChildModel]
