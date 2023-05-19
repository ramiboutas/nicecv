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
        formset=BaseInlineFormSet,
        can_order=False,
        can_delete=False,
        extra=1,
    )


def build_widgets(
    form: object,
    fields: list = [],
    widget_types: dict = {},
    html_class: str = None,
    x_bind_class: str = None,
    hx_post: str = None,
    hx_trigger: str = None,
):
    # Gather all html and frontend attributes
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

    # Set this attrs to the fields
    for field_name in fields:
        try:
            form.fields[field_name].widget.attrs.update(attrs)
        except Exception:
            raise Exception(f"Exception by setting attrs to the field {field_name}")

    # Set widget types
    for field_name, input_type in widget_types.items():
        try:
            form.fields[field_name].widget.input_type = input_type
        except Exception:
            raise Exception(
                f"Exception by setting the field {field_name} to {input_type}"
            )


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
        build_widgets(
            self,
            fields=["text"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            hx_post=hx_post,
            hx_trigger=settings.HTML_FORMS["textinput"]["hx_trigger"],
        )

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
        build_widgets(
            self,
            fields=self.Meta.fields,
            html_class=settings.HTML_FORMS["checkbox"]["class"],
        )

    class Meta(BaseSettingForm.Meta):
        model = models.ActivationSettings
        fields = ["photo", "jobtitle", "website", "description", "skill_set"]


class LabelSettingsForm(BaseSettingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_widgets(
            self,
            fields=self.Meta.fields,
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
        )

    class Meta(BaseSettingForm.Meta):
        model = models.LabelSettings
        fields = ["website", "description", "skill_set"]


# profile child formsets


class BaseChildFormSet(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            has_level = "level" in self.__class__.Meta.fields
            if has_level:
                build_widgets(
                    self,
                    fields=["level"],
                    widget_types={"level": "range"},
                    html_class=settings.HTML_FORMS["rangeinput"]["class"],
                )

        except Exception:
            pass


class SkillForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_widgets(
            self,
            fields=["name"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
        )

    class Meta:
        fields = ["name", "level"]
        model = models.Skill
