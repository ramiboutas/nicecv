import sys
import inspect
from functools import cache

from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet
from django.forms import HiddenInput
from django.utils.safestring import mark_safe
from django.conf import settings

from apps.profiles import models


@cache
def get_forms(singles=False, inlines=False, settings=False, get_all=False) -> dict:
    out = {}

    Forms = [k for _, k in inspect.getmembers(sys.modules[__name__], inspect.isclass)]

    if singles or get_all:
        out = out | {F.Meta.model: F for F in Forms if BaseChildForm in F.__bases__}

    if settings or get_all:
        out = out | {F.Meta.model: F for F in Forms if BaseSettingForm in F.__bases__}

    if inlines or get_all:
        out = out | {F.Meta.model: F for F in Forms if BaseChildFormSet in F.__bases__}

    return out


@cache
def get_model_and_form(Klass):
    """Returns a tuple: ChildModel, ChildModelForm"""
    Model = getattr(models, Klass) if isinstance(Klass, str) else Klass
    modelforms = get_forms(get_all=True)
    return Model, modelforms[Model]


@cache
def get_inlineformset(FormKlass):
    return inlineformset_factory(
        models.Profile,
        FormKlass.Meta.model,
        form=FormKlass,
        formset=BaseChildInlineFormSet,
        can_order=True,
        can_delete=False,
        extra=1,
    )


def build_widget_attrs(
    html_class=None, x_bind_class=None, hx_post=None, hx_trigger=None
):
    attrs = {}

    if html_class:
        # html class
        attrs = attrs | {"class": mark_safe(html_class)}

    if x_bind_class:
        # alpinejs :class attr.
        attrs = attrs | {":class": mark_safe(x_bind_class)}

    if hx_post:
        # htmx hx-post method
        attrs = attrs | {"hx-post": mark_safe(hx_post)}

    if hx_trigger:
        # htmx hx-trigger method
        attrs = attrs | {"hx-trigger": mark_safe(hx_trigger)}

    return attrs


def set_widget_attrs(form, attrs: dict, fields: list = None):
    """Sets widget attributes to a list of fields of a form .
    If 'fields' is not provided: tries with all form fields"""
    field_list = form.fields if fields is None else fields
    for field_name in field_list:
        try:
            form.fields[field_name].widget.attrs.update(attrs)
        except KeyError:
            pass


def set_widget_types(form, widget_types={}):
    """Sets the widget types of a form mapping the field name and its type"""
    for field_name, input_type in widget_types.items():
        try:
            form.fields[field_name].widget.input_type = input_type
        except KeyError:
            pass


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = ["public"]


# profile child forms


class BaseChildForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get("instance", None)
        hx_post = "" if obj is None else obj.update_form_url()
        attrs = build_widget_attrs(
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            hx_post=hx_post,
            hx_trigger=settings.HTML_FORMS["textinput"]["hx_trigger"],
        )
        set_widget_attrs(self, attrs)

    class Meta:
        fields = ["text"]


class FullnameForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Fullname


class JobtitleForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Jobtitle


class LocationForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Location


class BirthForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Birth


class PhoneForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Phone


class EmailForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Email


class WebsiteForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Website


class DescriptionForm(BaseChildForm):
    class Meta(BaseChildForm.Meta):
        model = models.Description


# profile settings


class BaseSettingForm(ModelForm):
    class Meta(ModelForm):
        fields = "__all__"
        exclude = ["profile"]


class ActivationSettingsForm(BaseSettingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(html_class=settings.HTML_FORMS["checkbox"]["class"])
        set_widget_attrs(self, attrs)

    class Meta(BaseSettingForm.Meta):
        model = models.ActivationSettings


class LabelSettingsForm(BaseSettingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
        )
        set_widget_attrs(self, attrs)

    class Meta(BaseSettingForm.Meta):
        model = models.LabelSettings


# profile child formsets


class BaseChildFormSet(ModelForm):
    class Meta:
        pass
        # widgets = {"order": forms.HiddenInput()}


class BaseChildInlineFormSet(BaseInlineFormSet):
    def get_ordering_widget(self):
        return HiddenInput(attrs={"class": "hidden"})

    def instance_forms(self):
        # not working, check another way
        return [form for form in self.forms if form.instance]


class SkillForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_input_attrs = build_widget_attrs(
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
        )

        slider_attrs = build_widget_attrs(html_class="range pr-6 accent-red-500")

        set_widget_attrs(self, text_input_attrs, fields=["name"])
        set_widget_attrs(self, slider_attrs, fields=["level"])
        set_widget_types(self, widget_types={"level": "range"})

    class Meta(BaseChildFormSet.Meta):
        fields = ["name", "level"]
        model = models.Skill
