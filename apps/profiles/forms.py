from django.forms import ModelForm
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet
from django.forms import HiddenInput
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
from .models import LabelSettings
from .models import ActivationSettings
from .models import Skill

# text input html attributes
INPUT_CLASS = "border-1 rounded-md hover:bg-indigo-100 border-indigo-100"
INPUT_XBIND_CLASS = "active ? 'border-indigo-400' : 'border-indigo-100'"
INPUT_HX_TRIGGER = "keyup changed delay:2s, change"
# checkbox html attributes
CHECKBOX_CLASS = "h-4 w-4 rounded border-indigo-400 focus:ring-indigo-400"


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
        model = Profile
        fields = ["public"]


# profile child forms


class ChildForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get("instance", None)
        hx_post = "" if obj is None else obj.update_form_url()
        attrs = build_widget_attrs(
            html_class=INPUT_CLASS,
            x_class=INPUT_XBIND_CLASS,
            hx_post=hx_post,
            hx_trigger=INPUT_HX_TRIGGER,
        )
        set_widget_attrs(self, attrs)

    class Meta:
        fields = ["text"]


class FullnameForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Fullname


class JobtitleForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Jobtitle


class LocationForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Location


class BirthForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Birth


class PhoneForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Phone


class EmailForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Email


class WebsiteForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Website


class DescriptionForm(ChildForm):
    class Meta(ChildForm.Meta):
        model = Description


# profile settings


class SettingsForm(ModelForm):
    class Meta(ModelForm):
        fields = "__all__"
        exclude = ["profile"]


class ActivationSettingsForm(SettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(html_class=CHECKBOX_CLASS)
        set_widget_attrs(self, attrs)

    class Meta(SettingsForm.Meta):
        model = ActivationSettings


class LabelSettingsForm(SettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(html_class=INPUT_CLASS, x_class=INPUT_XBIND_CLASS)
        set_widget_attrs(self, attrs)

    class Meta(SettingsForm.Meta):
        model = LabelSettings


# profile child formsets


class ChildSetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(html_class=INPUT_CLASS, x_class=INPUT_XBIND_CLASS)
        set_widget_attrs(self, attrs)
        set_widget_types(self, widget_types={"level": "range"})

    class Meta:
        pass
        # exclude = ["profile"]


class BaseChildFormSet(BaseModelFormSet):
    def __init__(self, profile=None, update_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_url = update_url
        if profile:
            self.profile = profile
            self.queryset = self.model.objects.filter(profile=profile)

    def get_ordering_widget(self):
        return HiddenInput(attrs={"class": "sortable"})


class SkillForm(ChildSetForm):
    class Meta(ChildSetForm.Meta):
        fields = ["name", "level"]
        model = Skill


SkillFormSet = modelformset_factory(
    Skill,
    form=SkillForm,
    formset=BaseChildFormSet,
    can_order=False,
    can_delete=False,
    extra=0,
)
