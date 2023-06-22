import time
import uuid
from functools import cache

import auto_prefetch
import factory
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from PIL import Image

from ..tex.filters import do_latex_escape
from .languages import Language


def get_photo_upload_path(profile, filename):
    return f"profiles/{profile.category}/{profile.id}/photos/{filename}"


class Profile(auto_prefetch.Model):
    """
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile
    """

    PROFILE_CATEGORIES = (
        ("temporal", _("Temporal")),
        ("user", _("User profile")),
        ("template", _("Template")),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="profile_set",
        null=True,
        blank=True,
    )
    session = auto_prefetch.ForeignKey(
        Session,
        related_name="profile_set",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    category = models.CharField(
        max_length=16,
        choices=PROFILE_CATEGORIES,
        default="user",
    )

    language_setting = auto_prefetch.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
    )
    public = models.BooleanField(default=False)
    auto_created = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, max_length=16, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # input fields from user
    fullname = models.CharField(
        _("Full name"),
        null=True,
        max_length=64,
    )
    jobtitle = models.CharField(
        _("Job title"),
        max_length=64,
        null=True,
    )
    location = models.CharField(
        _("Location"),
        max_length=64,
        null=True,
    )
    birth = models.CharField(
        _("Birth"),
        max_length=64,
        null=True,
    )
    phone = models.CharField(
        _("Phone number"),
        max_length=64,
        null=True,
    )
    email = models.EmailField(
        _("Full name"),
        max_length=64,
        null=True,
    )
    website = models.URLField(
        _("Website"),
        max_length=32,
        null=True,
    )
    about = models.TextField(
        max_length=2048,
        null=True,
    )
    about_rows = models.PositiveSmallIntegerField(default=15)

    # activation fields and objects
    photo_active = models.BooleanField(
        default=True,
        verbose_name=_("Photo"),
    )
    jobtitle_active = models.BooleanField(
        default=True,
        verbose_name=_("Job title"),
    )
    location_active = models.BooleanField(
        default=False,
        verbose_name=_("Location"),
    )
    birth_active = models.BooleanField(
        default=False,
        verbose_name=_("Birth date"),
    )
    phone_active = models.BooleanField(
        default=True,
        verbose_name=_("Phone number"),
    )
    email_active = models.BooleanField(
        default=True,
        verbose_name=_("Email address"),
    )
    website_active = models.BooleanField(
        default=False,
        verbose_name=_("Website"),
    )
    about_active = models.BooleanField(
        default=True,
        verbose_name=_("About me"),
    )
    skill_active = models.BooleanField(
        default=True,
        verbose_name=_("Skills"),
    )
    language_active = models.BooleanField(
        default=False,
        verbose_name=_("Languages"),
    )
    education_active = models.BooleanField(
        default=True,
        verbose_name=_("Education"),
    )
    experience_active = models.BooleanField(
        default=True,
        verbose_name=_("Work experience"),
    )
    achievement_active = models.BooleanField(
        default=False,
        verbose_name=_("Achievements"),
    )
    project_active = models.BooleanField(
        default=False,
        verbose_name=_("Projects"),
    )
    publication_active = models.BooleanField(
        default=False,
        verbose_name=_("Publications"),
    )

    fullname_label = models.CharField(max_length=32, default=_("Full name"))
    jobtitle_label = models.CharField(max_length=32, default=_("Job title"))
    location_label = models.CharField(max_length=32, default=_("Location"))
    birth_label = models.CharField(max_length=32, default=_("Birth date"))
    phone_label = models.CharField(max_length=32, default=_("Phone number"))
    email_label = models.CharField(max_length=32, default=_("Email address"))
    website_label = models.CharField(max_length=32, default=_("Website"))
    about_label = models.CharField(max_length=32, default=_("About me"))
    skill_label = models.CharField(max_length=32, default=_("Skills"))
    language_label = models.CharField(max_length=32, default=_("Languages"))
    education_label = models.CharField(max_length=32, default=_("Education"))
    experience_label = models.CharField(max_length=32, default=_("Work experience"))
    achievement_label = models.CharField(max_length=32, default=_("Achievements"))
    project_label = models.CharField(max_length=32, default=_("Projects"))
    publication_label = models.CharField(max_length=32, default=_("Publications"))

    full_photo = models.ImageField(null=True, upload_to=get_photo_upload_path)
    cropped_photo = models.ImageField(null=True, upload_to=get_photo_upload_path)
    crop_x = models.PositiveSmallIntegerField(null=True, blank=True)
    crop_y = models.PositiveSmallIntegerField(null=True, blank=True)
    crop_width = models.PositiveSmallIntegerField(null=True, blank=True)
    crop_height = models.PositiveSmallIntegerField(null=True, blank=True)

    def get_tex_value(self, field_name):
        field = getattr(self, field_name, None)
        return do_latex_escape(field) if field else ""

    @cached_property
    def upload_photo_url(self):
        return reverse("profiles:upload-photo", kwargs={"id": self.id})

    @cached_property
    def crop_photo_url(self):
        return reverse("profiles:crop-photo", kwargs={"id": self.id})

    @cached_property
    def delete_photos_url(self):
        return reverse("profiles:delete-photos", kwargs={"id": self.id})

    def update_url(self, params=None):
        url = reverse("profiles:update", kwargs={"id": self.id})
        extra = (
            "?" + "&".join([f"{k}={v}" for k, v in params.items()])
            if bool(params)
            else ""
        )
        return url + extra

    def update_formset_url(self, Klass):
        return reverse(
            "profiles:update-formset", kwargs={"klass": Klass.__name__, "id": self.id}
        )

    @cached_property
    def update_fields_url(self):
        return reverse("profiles:update-fields", kwargs={"id": self.id})

    @cached_property
    def update_labelling_url(self):
        return reverse(
            "profiles:update-settings",
            kwargs={"klass": "LabellingForm", "id": self.id},
        )

    @cached_property
    def update_activation_url(self):
        return reverse(
            "profiles:update-settings",
            kwargs={"klass": "ActivationForm", "id": self.id},
        )

    def order_formset_url(self, Klass):
        return reverse(
            "profiles:order-formset", kwargs={"klass": Klass.__name__, "id": self.id}
        )

    @cached_property
    def update_skill_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Skill)

    @cached_property
    def order_skill_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Skill)

    @cached_property
    def update_language_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(LanguageAbility)

    @cached_property
    def order_language_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(LanguageAbility)

    @cached_property
    def update_education_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Education)

    @cached_property
    def order_education_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Education)

    @cached_property
    def update_experience_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Experience)

    @cached_property
    def order_experience_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Experience)

    @cached_property
    def update_achievement_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Achievement)

    @cached_property
    def order_achievement_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Achievement)

    @cached_property
    def update_project_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Project)

    @cached_property
    def order_project_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Project)

    @cached_property
    def update_publication_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Publication)

    @cached_property
    def order_publication_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Publication)

    @cached_property
    def delete_object_url(self):
        return reverse("profiles:delete", kwargs={"id": self.id})

    def collect_context(self) -> dict:
        from ..forms import profiles

        context = {
            "profile": self,
            "personal_info_form": profiles.ProfileFieldForm(instance=self),
            "activation_form": profiles.ActivationForm(instance=self),
            "labelling_form": profiles.LabellingForm(instance=self),
            "uploadphoto_form": profiles.UploadPhotoForm(instance=self),
            "cropphoto_form": profiles.CropPhotoForm(instance=self),
        }

        # one to many children as formsets
        for Model, Form in profiles.get_inlineforms().items():
            name = Model._meta.model_name + "_formset"
            context[name] = profiles.create_inlineformset(Form)(instance=self)

        return context

    def build_xml(self):
        # TODO: build xml for the deepl API
        # https://www.deepl.com/docs-api/xml/
        # https://stackoverflow.com/questions/36021526/converting-an-array-dict-to-xml-in-python
        pass

    def crop_photo(self):
        if self.full_photo:
            self.cropped_photo.save(
                "cropped_" + self.full_photo.name.split("/")[-1],
                ContentFile(self.full_photo.read()),
                save=False,
            )
            image = Image.open(self.cropped_photo)
            cropping_area = (
                self.crop_x,
                self.crop_y,
                self.crop_x + self.crop_width,
                self.crop_y + self.crop_height,
            )
            cropped_image = image.crop(cropping_area)
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(self.cropped_photo.path, save=False)
            self.save()

    def process_photo(self):
        if self.full_photo:
            size_modified = False
            try:
                img = Image.open(self.full_photo)
            except Exception as e:
                raise e

            if img.height > 1200 or img.width > 1200:
                new_size = (1200, 1200)
                img.thumbnail(new_size)
                img.save(self.full_photo.path)
                size_modified = True

            if not self.cropped_photo:
                if size_modified:
                    img = Image.open(self.full_photo)
                distance = int(0.95 * min([img.height, img.width]))
                self.crop_width, self.crop_height = distance, distance
                self.crop_x = int((img.width - distance) / 2)
                self.crop_y = int((img.height - distance) / 2)
                self.save()

    @cached_property
    def has_photo(self):
        to_check = getattr(getattr(self, "cropped_photo"), "name")
        return to_check != "" and to_check is not None

    @cached_property
    def photo_path(self):
        if self.has_photo:
            return self.cropped_photo.path

    def __str__(self):
        return f"{self.category.capitalize()} Profile ({self.fullname} - {self.language_setting})"

    @classmethod
    def create_template_profiles(cls):
        from ..factories.profiles import ProfileFactory

        cls.objects.filter(auto_created=True).delete()

        for lang_obj in [Language.get(lang[0]) for lang in settings.LANGUAGES]:
            with factory.Faker.override_default_locale(lang_obj.code):
                obj = ProfileFactory(language_setting=lang_obj)
                print(f"✅ {obj} created.")

    def fetch_cvs(self):
        start = time.time()
        from .cvs import Cv
        from .tex import Tex

        cvs = []

        for tex in Tex.objects.all():
            try:
                cv = Cv.objects.get(tex=tex, profile=self)
            except Cv.DoesNotExist:
                cv = Cv.objects.filter(
                    profile__category="template",
                    profile__language_setting=self.language_setting,
                )[0]
            cvs.append(cv)
        return cvs

    def save(self, *args, **kwargs):
        if self.about:
            rows = int(len(self.about) / 35)
            self.about_rows = rows if rows > 3 else 3
        super().save(*args, **kwargs)


class LevelMethodsMixin:
    @property
    def level_base_5_int(self):
        return round(self.level * 5 / 100)

    @property
    def level_base_6_float(self):
        return self.level * 6 / 100


class AbstractChildSet(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=1)

    def get_delete_url(self):
        cls = type(self).__name__
        return reverse("profiles:delete-child", kwargs={"klass": cls, "id": self.id})

    def get_tex_value(self, field_name):
        field = getattr(self, field_name, None)
        return do_latex_escape(field) if field else ""

    def save(self, *args, **kwargs):
        if not self.pk:
            last = type(self).objects.filter(profile=self.profile).last()
            self.order = last.order + 1 if last else 1
        super().save(*args, **kwargs)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ("order",)


# Profile settings models


class Skill(AbstractChildSet, LevelMethodsMixin):
    name = models.CharField(
        "📊 " + _("Skill"),
        max_length=50,
    )
    level = models.IntegerField(
        _("Level"),
        default=50,
    )

    def __str__(self):
        return self.name


class LanguageAbility(AbstractChildSet, LevelMethodsMixin):
    """
    An object representing the languages that the member holds.
    """

    name = models.CharField(
        "🗣️ " + _("Language"),
        max_length=50,
    )
    level = models.IntegerField(
        _("Level"),
        default=50,
    )

    def __str__(self):
        return self.name


class AbstractModelWithDatesAndDescription(auto_prefetch.Model):
    start_date = models.CharField(
        "🗓️ " + _("Start date"),
        max_length=16,
    )
    end_date = models.CharField(
        "🗓️ " + _("End date"),
        max_length=16,
    )
    description = models.TextField(
        "📝 " + _("What did you learn?"),
        null=True,
        blank=True,
        max_length=1024,
    )
    rows = models.PositiveSmallIntegerField(default=10)

    def save(self, *args, **kwargs):
        rows = int(len(self.description) / 80)
        self.rows = rows if rows > 3 else 3
        super().save(*args, **kwargs)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


class Education(AbstractChildSet, AbstractModelWithDatesAndDescription):
    """
    An object representing the member's educational background.
    See Education Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/education
    """

    title = models.CharField(
        "🎓 " + _("Title"),
        max_length=64,
    )
    institution = models.CharField(
        "🏫 " + _("Institution"),
        max_length=32,
    )

    class Meta(AbstractChildSet.Meta):
        verbose_name_plural = _("Education")


class Experience(AbstractChildSet, AbstractModelWithDatesAndDescription):
    """
    Employment history. See Positions for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position
    """

    title = models.CharField(
        "🧑‍💼 " + _("Job title"),
        null=True,
        blank=True,
        max_length=64,
    )
    location = models.CharField(
        "📍 " + _("Location"),
        max_length=32,
    )
    company = models.CharField(
        "🏢 " + _("Company name"),
        max_length=32,
    )

    class Meta(AbstractChildSet.Meta):
        verbose_name_plural = _("Experience")

    def __str__(self):
        return self.title


class Achievement(AbstractChildSet):
    """Archivement object"""

    title = models.CharField(
        "🏆 " + _("Goal achieved"),
        max_length=64,
    )
    date = models.CharField(
        "🗓️ " + _("Date"),
        null=True,
        blank=True,
        max_length=16,
    )


class Project(AbstractChildSet):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
    """

    title = models.CharField(
        "🌍 " + _("Project name"),
        max_length=64,
    )
    role = models.CharField(
        "🧑‍💼 " + _("Role in the project"),
        null=True,
        blank=True,
        max_length=32,
    )
    organization = models.CharField(
        "🤝 " + _("Organization"),
        null=True,
        blank=True,
        max_length=64,
    )
    link = models.CharField(
        "🔗 " + _("Link"),
        null=True,
        blank=True,
        max_length=128,
    )


class Publication(AbstractChildSet):
    """
    An object representing the various publications associated with the member.
    See Publication Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication
    """

    date = models.CharField(
        "🗓️ " + _("Date"),
        null=True,
        blank=True,
        max_length=16,
    )
    title = models.CharField(
        "🔬 " + _("Publication title"),
        max_length=128,
    )
    authors = models.CharField(
        "👥 " + _("Authors"),
        null=True,
        blank=True,
        max_length=64,
    )
    publisher = models.CharField(
        "📑 " + _("Publisher"),
        null=True,
        blank=True,
        max_length=32,
    )

    # try not to include
    link = models.URLField(
        "🔗 " + _("Link"),
        null=True,
        blank=True,
        max_length=128,
    )
