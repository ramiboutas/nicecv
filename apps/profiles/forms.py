import inspect
import sys
from functools import cache

from django.conf import settings
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from apps.core.exceptions import ErrorBySettingFormFieldAttributes
from apps.core.exceptions import ErrorBySettingFormWidgetInputType
from apps.profiles import models


@cache
def get_inlineforms() -> dict:
    Forms = [k for _, k in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
    return {F.Meta.model: F for F in Forms if BaseChildFormSet in F.__bases__}


@cache
def get_model_and_form(Klass):
    """Returns a tuple: ChildModel, ChildModelForm"""
    Model = getattr(models, Klass) if isinstance(Klass, str) else Klass
    modelforms = get_inlineforms()
    return Model, modelforms[Model]


@cache
def create_inlineformset(Form):
    return inlineformset_factory(
        models.Profile,
        Form.Meta.model,
        form=Form,
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
    html_autocomplete=None,
    html_rows: str = None,
    x_bind_class: str = None,
    hx_post: str = None,
    hx_trigger: str = None,
    hx_swap: str = None,
):
    # Gather all html and frontend attributes
    attrs = {}

    if html_class:
        # html class
        attrs = attrs | {"class": mark_safe(html_class)}

    if html_autocomplete:
        # HTML attribute: autocomplete
        # https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
        attrs = attrs | {"autocomplete": mark_safe(html_autocomplete)}

    if x_bind_class:
        # alpinejs :class attr.
        attrs = attrs | {":class": mark_safe(x_bind_class)}

    if html_rows:
        attrs = attrs | {"rows": mark_safe(html_rows)}

    if hx_post:
        # htmx hx-post method
        attrs = attrs | {"hx-post": mark_safe(hx_post)}

    if hx_trigger:
        # htmx hx-trigger method
        attrs = attrs | {"hx-trigger": mark_safe(hx_trigger)}

    if hx_swap:
        # htmx hx-trigger method
        attrs = attrs | {"hx-swap": mark_safe(hx_swap)}

    # Set this attrs to the fields
    for field_name in fields:
        try:
            form.fields[field_name].widget.attrs.update(attrs)
        except ErrorBySettingFormFieldAttributes as e:
            e.add_note(f"Exception by setting attrs to the field {field_name}")
            raise e

    # Set widget types
    for field_name, input_type in widget_types.items():
        try:
            form.fields[field_name].widget.input_type = input_type
        except ErrorBySettingFormWidgetInputType as e:
            e.add_note(f"Exception by setting attrs to the field {field_name}")
            raise e


class PersonalInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = kwargs.get("instance", None)

        build_widgets(
            self,
            fields=["fullname", "jobtitle", "location", "birth", "phone", "email"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            hx_post=profile.update_personal_info_url(),
            hx_trigger="keyup changed delay:3s, change",
            hx_swap="none",
        )
        build_widgets(
            self,
            fields=["about"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            html_rows=profile.about_rows,
            html_autocomplete="off",
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            hx_post=profile.update_field_url(),
            hx_trigger="keyup changed delay:2s",
            hx_swap="none",
        )

    class Meta:
        model = models.Profile
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

        build_widgets(
            self,
            fields=self.Meta.fields,
            html_class=settings.HTML_FORMS["checkbox"]["class"],
        )

    class Meta:
        model = models.Profile
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

        build_widgets(
            self,
            fields=self.Meta.fields,
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
        )

    class Meta:
        model = models.Profile
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
        build_widgets(
            self,
            fields=["full_photo"],
            html_class=settings.HTML_FORMS["fileinput"]["class"],
        )

    class Meta:
        model = models.Profile
        fields = ["full_photo"]


class CropPhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_widgets(
            self,
            widget_types={
                "crop_x": "hidden",
                "crop_y": "hidden",
                "crop_width": "hidden",
                "crop_height": "hidden",
            },
        )

    class Meta:
        model = models.Profile
        fields = ["crop_x", "crop_y", "crop_width", "crop_height"]


# profile child formsets


class BaseChildFormSet(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "level" in getattr(type(self).Meta, "fields", None):
            build_widgets(
                self,
                fields=["level"],
                widget_types={"level": "range"},
                html_class=settings.HTML_FORMS["rangeinput"]["class"],
            )


class SkillForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_widgets(
            self,
            fields=["name"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )

    class Meta:
        fields = ["name", "level"]
        model = models.Skill


class LanguageForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_widgets(
            self,
            fields=["name"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )

    class Meta:
        fields = ["name", "level"]
        model = models.Language


class EducationForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get("instance", None)
        rows = getattr(obj, "rows", 3)
        build_widgets(
            self,
            fields=["title", "institution", "start_date", "end_date"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )
        build_widgets(
            self,
            fields=["description"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_rows=rows,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["start_date", "end_date", "title", "institution", "description"]
        model = models.Education


class ExperienceForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get("instance", None)
        rows = getattr(obj, "rows", 3)
        build_widgets(
            self,
            fields=["title", "company", "start_date", "end_date"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )
        build_widgets(
            self,
            fields=["description"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_rows=rows,
            html_autocomplete="off",
        )

    class Meta:
        fields = ["start_date", "end_date", "title", "company", "description"]
        model = models.Experience


class AchievementForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_widgets(
            self,
            fields=["title", "date"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )

    class Meta:
        fields = ["date", "title"]
        model = models.Achievement


class ProjectForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        build_widgets(
            self,
            fields=["role", "title", "organization", "link"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )

    class Meta:
        fields = ["title", "role", "organization", "link"]
        model = models.Project


class PublicationForm(BaseChildFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        build_widgets(
            self,
            fields=["date", "title", "publisher", "link"],
            html_class=settings.HTML_FORMS["textinput"]["class"],
            x_bind_class=settings.HTML_FORMS["textinput"]["x_bind_class"],
            html_autocomplete="off",
        )

    class Meta:
        fields = ["date", "title", "publisher", "link"]
        model = models.Publication
