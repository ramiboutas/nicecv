import warnings

from django.forms import ModelForm
from django.forms import formset_factory
from django.forms import BaseFormSet
from django.forms.widgets import Input

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
INPUT_HX_TRIGGER = "keyup changed delay:2s"
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
    field_list = form.fields if fields is None else fields
    for field_name in field_list:
        try:
            form.fields[field_name].widget.attrs.update(attrs)
        except KeyError:
            pass


class RangeInput(Input):
    input_type = "range"
    template_name = "django/forms/widgets/number.html"


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["public"]


class SingleItemChildForm(ModelForm):
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


class FullnameForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Fullname


class JobtitleForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Jobtitle


class LocationForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Location


class BirthForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Birth


class PhoneForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Phone


class EmailForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Email


class WebsiteForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Website


class DescriptionForm(SingleItemChildForm):
    class Meta(SingleItemChildForm.Meta):
        model = Description


class ProfileSettingsForm(ModelForm):
    pass


class ActivationSettingsForm(ProfileSettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(html_class=CHECKBOX_CLASS)
        set_widget_attrs(self, attrs)

    class Meta(ModelForm):
        fields = "__all__"
        exclude = ["profile"]
        model = ActivationSettings


class LabelSettingsForm(ProfileSettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(html_class=INPUT_CLASS, x_class=INPUT_XBIND_CLASS)
        set_widget_attrs(self, attrs)

    class Meta(ModelForm):
        fields = "__all__"
        exclude = ["profile"]
        model = LabelSettings


class SkillForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = build_widget_attrs(html_class=INPUT_CLASS, x_class=INPUT_XBIND_CLASS)
        set_widget_attrs(self, attrs, fields=["name"])
        self.fields["level"].widget = RangeInput()

    class Meta(ModelForm):
        fields = "__all__"
        exclude = ["profile"]
        model = Skill


class BaseChildItemFormSet(BaseFormSet):
    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)


SkillFormSet = formset_factory(
    SkillForm, formset=BaseChildItemFormSet, can_order=False, can_delete=False
)
