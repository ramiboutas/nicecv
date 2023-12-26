import inspect
import sys
from functools import cache

from django.conf import settings
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory
from django.forms import ModelForm

from ..models import profiles
from ..utils import build_form_widgets


# text input attrs
TEXTINPUT_CLASS = (
    "px-2 w-full rounded-md border-transparent focus:border-transparent focus:ring-0"
)
TEXTINPUT_X_BIND_CLASS = "active ? 'bg-indigo-200' : ''"
TEXTINPUT_HX_TRIGGER = "keyup changed delay:1s, change"
TEXTINPUT_LABEL_CLASS = (
    "absolute -top-2 left-2 inline-block px-1 text-xs font-medium text-gray-400"
)
TEXTINPUT_LABEL_X_BIND_CLASS = "active ? ' bg-indigo-200' : ''"

# range input attrs
RANGEINPUT_CLASS = "w-full"

# check box input attrs
CHECKBOX_CLASS = (
    "h-4 w-4 rounded border-indigo-600 focus:ring-indigo-400 accent-indigo-600"
)

# file input attrs
FILEINPUT_CLASS = "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"


@cache
def get_inlineforms() -> dict:
    Forms = [k for _, k in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
    return {F.Meta.model: F for F in Forms if BaseChildFormSet in F.__bases__}


@cache
def get_child_model_and_form(Klass):
    """Returns a tuple: ChildModel, ChildModelForm"""
    Model = getattr(profiles, Klass) if isinstance(Klass, str) else Klass
    modelforms = get_inlineforms()
    return Model, modelforms[Model]


@cache
def create_inlineformset(Form):
    return inlineformset_factory(
        profiles.Profile,
        Form.Meta.model,
        form=Form,
        formset=BaseInlineFormSet,
        can_order=False,
        can_delete=False,
        extra=1,
    )


class ProfileFieldForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = kwargs.get("instance", None)

        build_form_widgets(
            self,
            fields=[
                "fullname",
                "jobtitle",
                "location",
                "birth",
                "phone",
                "email",
                "website",
                "language_code",
            ],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            hx_post=profile.update_fields_url,
            hx_trigger="keyup changed delay:3s, change",
            hx_swap="none",
        )
        build_form_widgets(
            self,
            fields=["about"],
            html_class=TEXTINPUT_CLASS,
            html_rows=profile.about_rows,
            html_autocomplete="off",
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            hx_post=profile.update_fields_url,
            hx_trigger="keyup changed delay:5s, change",
            hx_swap="none",
        )

    class Meta:
        model = profiles.Profile
        fields = [
            "fullname",
            "jobtitle",
            "location",
            "birth",
            "phone",
            "email",
            "website",
            "about",
            "language_code",
        ]


class ActivationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_form_widgets(
            self,
            fields=self.Meta.fields,
            html_class=CHECKBOX_CLASS,
        )

    class Meta:
        model = profiles.Profile
        fields = [
            "photo_active",
            "jobtitle_active",
            "website_active",
            "about_active",
            "skill_active",
            "language_active",
            "education_active",
            "experience_active",
            "achievement_active",
            "project_active",
            "publication_active",
        ]


class LabellingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_form_widgets(
            self,
            fields=self.Meta.fields,
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
        )

    class Meta:
        model = profiles.Profile
        fields = [
            "fullname_label",
            "jobtitle_label",
            "location_label",
            "birth_label",
            "phone_label",
            "email_label",
            "website_label",
            "about_label",
            "skill_label",
            "language_label",
            "education_label",
            "experience_label",
            "achievement_label",
            "project_label",
            "publication_label",
        ]


# profile child forms


class UploadPhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_form_widgets(
            self,
            fields=["full_photo"],
            html_class=FILEINPUT_CLASS,
        )

    class Meta:
        model = profiles.Profile
        fields = ["full_photo"]


class CropPhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_form_widgets(
            self,
            widget_types={
                "crop_x": "hidden",
                "crop_y": "hidden",
                "crop_width": "hidden",
                "crop_height": "hidden",
            },
        )

    class Meta:
        model = profiles.Profile
        fields = ["crop_x", "crop_y", "crop_width", "crop_height"]


# profile child formsets


class BaseChildFormSet(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "level" in getattr(type(self).Meta, "fields", None):
            build_form_widgets(
                self,
                fields=["level"],
                widget_types={"level": "range"},
                html_class=RANGEINPUT_CLASS,
            )


class SkillForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_form_widgets(
            self,
            fields=["name"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["name", "level"]
        model = profiles.Skill


class LanguageAbilityForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_form_widgets(
            self,
            fields=["name"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["name", "level"]
        model = profiles.LanguageAbility


class EducationForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get("instance", None)
        rows = getattr(obj, "rows", 3)
        build_form_widgets(
            self,
            fields=["title", "institution", "start_date", "end_date"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_autocomplete="off",
        )
        build_form_widgets(
            self,
            fields=["description"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_rows=rows,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["start_date", "end_date", "title", "institution", "description"]
        model = profiles.Education


class ExperienceForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get("instance", None)
        rows = getattr(obj, "rows", 3)
        build_form_widgets(
            self,
            fields=["title", "company", "start_date", "end_date"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_autocomplete="off",
        )
        build_form_widgets(
            self,
            fields=["description"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_rows=rows,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["start_date", "end_date", "title", "company", "description"]
        model = profiles.Experience


class AchievementForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_form_widgets(
            self,
            fields=["title", "date"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["date", "title"]
        model = profiles.Achievement


class ProjectForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_form_widgets(
            self,
            fields=["role", "title", "organization", "link"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["title", "role", "organization", "link"]
        model = profiles.Project


class PublicationForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_form_widgets(
            self,
            fields=["date", "title", "authors", "publisher", "link"],
            html_class=TEXTINPUT_CLASS,
            x_bind_class=TEXTINPUT_X_BIND_CLASS,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["date", "title", "publisher", "authors", "link"]
        model = profiles.Publication
