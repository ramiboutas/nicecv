import sys
import inspect
from functools import cache

from django.conf import settings
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory
from django.forms import ModelForm

from ..utils import build_form_widgets
from ..models import profiles


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
            fields=["fullname", "jobtitle", "location", "birth", "phone", "email"],
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
            hx_post=profile.update_fields_url(),
            hx_trigger="keyup changed delay:3s, change",
            hx_swap="none",
        )
        build_form_widgets(
            self,
            fields=["about"],
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            html_rows=profile.about_rows,
            html_autocomplete="off",
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
            hx_post=profile.update_fields_url(),
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
            "about",
        ]


class ActivationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_form_widgets(
            self,
            fields=self.Meta.fields,
            html_class=settings.FORM_ATTRIBUTES["checkbox"]["class"],
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
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
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
            html_class=settings.FORM_ATTRIBUTES["fileinput"]["class"],
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
                html_class=settings.FORM_ATTRIBUTES["rangeinput"]["class"],
            )


class SkillForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_form_widgets(
            self,
            fields=["name"],
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
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
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
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
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )
        build_form_widgets(
            self,
            fields=["description"],
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
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
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )
        build_form_widgets(
            self,
            fields=["description"],
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
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
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
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
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
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
            fields=["date", "title", "publisher", "link"],
            html_class=settings.FORM_ATTRIBUTES["textinput"]["class"],
            x_bind_class=settings.FORM_ATTRIBUTES["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )

    class Meta:
        fields = ["date", "title", "publisher", "link"]
        model = profiles.Publication
