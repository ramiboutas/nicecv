import uuid
from functools import cache

import auto_prefetch
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from apps.core.models import Language


null_blank = {"null": True, "blank": True}
null_blank_8 = {"null": True, "blank": True, "max_length": 8}
null_blank_16 = {"null": True, "blank": True, "max_length": 16}
null_blank_32 = {"null": True, "blank": True, "max_length": 32}
null_blank_64 = {"null": True, "blank": True, "max_length": 34}
null_blank_128 = {"null": True, "blank": True, "max_length": 128}
null_blank_256 = {"null": True, "blank": True, "max_length": 256}
null_blank_528 = {"null": True, "blank": True, "max_length": 528}
null_blank_1024 = {"null": True, "blank": True, "max_length": 1024}

null_16 = {"null": True, "max_length": 16}
null_32 = {"null": True, "max_length": 32}
null_64 = {"null": True, "max_length": 34}
null_128 = {"null": True, "max_length": 128}
null_256 = {"null": True, "max_length": 256}
null_528 = {"null": True, "max_length": 528}
null_1024 = {"null": True, "max_length": 1024}


PROFILE_CATEGORIES = (
    ("temporal", _("Temporal")),
    ("user_profile", _("User profile")),
    ("template", _("Template")),
)


def get_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "profiles/{0}/{1}".format(instance.id, filename)


class Profile(auto_prefetch.Model):
    """
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="profile_set",
        **null_blank,
    )
    session = auto_prefetch.ForeignKey(
        Session,
        related_name="profile_set",
        on_delete=models.CASCADE,
        **null_blank,
    )
    category = models.CharField(
        max_length=16,
        choices=PROFILE_CATEGORIES,
        default="user_profile",
    )

    language_setting = auto_prefetch.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True
    )
    public = models.BooleanField(default=False)
    slug = models.SlugField(**null_blank_16, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # input fields from user
    fullname = models.CharField(**null_64)
    jobtitle = models.CharField(**null_64)
    location = models.CharField(**null_64)
    birth = models.CharField(**null_16)
    phone = models.CharField(**null_64)
    email = models.EmailField(**null_64)
    website = models.URLField(max_length=32, verbose_name=_("Website"))
    about = models.TextField(**null_1024)
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
        default=True,
        verbose_name=_("Location"),
    )
    birth_active = models.BooleanField(
        default=True,
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
        default=True,
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
        default=True, verbose_name=_("Work experience")
    )
    achievement_active = models.BooleanField(
        default=False, verbose_name=_("Achievements")
    )
    project_active = models.BooleanField(default=False, verbose_name=_("Projects"))
    publication_active = models.BooleanField(
        default=False, verbose_name=_("Publications")
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

    full_photo = models.ImageField(null=True, upload_to=get_upload_path)
    cropped_photo = models.ImageField(null=True, upload_to=get_upload_path)
    crop_x = models.PositiveSmallIntegerField(**null_blank)
    crop_y = models.PositiveSmallIntegerField(**null_blank)
    crop_width = models.PositiveSmallIntegerField(**null_blank)
    crop_height = models.PositiveSmallIntegerField(**null_blank)

    def upload_photo_url(self):
        return reverse("profiles:upload-photo", kwargs={"id": self.id})

    def crop_photo_url(self):
        return reverse("profiles:crop-photo", kwargs={"id": self.id})

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

    def update_fields_url(self):
        return reverse("profiles:update-fields", kwargs={"id": self.id})

    def update_labelling_url(self):
        return reverse(
            "profiles:update-settings",
            kwargs={"klass": "LabellingForm", "id": self.id},
        )

    def update_activation_url(self):
        return reverse(
            "profiles:update-settings",
            kwargs={"klass": "ActivationForm", "id": self.id},
        )

    def order_formset_url(self, Klass):
        return reverse(
            "profiles:order-formset", kwargs={"klass": Klass.__name__, "id": self.id}
        )

    def update_skill_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Skill)

    def order_skill_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Skill)

    def update_language_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Language)

    def order_language_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Language)

    def update_education_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Education)

    def order_education_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Education)

    def update_experience_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Experience)

    def order_experience_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Experience)

    def update_achievement_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Achievement)

    def order_achievement_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Achievement)

    def update_project_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Project)

    def order_project_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Project)

    def update_publication_url(self):
        """This method is made for being called from Templates"""
        return self.update_formset_url(Publication)

    def order_publication_url(self):
        """This method is made for being called from Templates"""
        return self.order_formset_url(Publication)

    def delete_object_url(self):
        return reverse("profiles:delete", kwargs={"id": self.id})

    def collect_context(self) -> dict:
        from apps.profiles import forms

        context = {
            "profile": self,
            "personal_info_form": forms.ProfileFieldForm(instance=self),
            "activation_form": forms.ActivationForm(instance=self),
            "labelling_form": forms.LabellingForm(instance=self),
            "uploadphoto_form": forms.UploadPhotoForm(instance=self),
            "cropphoto_form": forms.CropPhotoForm(instance=self),
        }

        # one to many children as formsets
        for Model, Form in forms.get_inlineforms().items():
            name = Model._meta.model_name + "_formset"
            context[name] = forms.create_inlineformset(Form)(instance=self)

        return context

    def get_tex_proxy(self):
        from apps.proxies.models import TexProfile

        return TexProfile.objects.get(id=self.id)

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
            resized_image.save(self.cropped_photo.path)
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

    def save(self, *args, **kwargs):
        if self.about:
            rows = int(len(self.about) / 35)
            self.about_rows = rows if rows > 3 else 3
        super().save(*args, **kwargs)


# proxy profile


# Abract models and mixins


class LevelMethodsMixin:
    @property
    def level_base_5_int(self):
        return (self.level * 5 / 100).__round__()

    @property
    def level_base_6_float(self):
        return self.level * 6 / 100


class AbstractChildSet(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    order = models.PositiveSmallIntegerField(default=1)

    def get_delete_url(self):
        cls = type(self).__name__
        return reverse("profiles:delete-child", kwargs={"klass": cls, "id": self.id})

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
    name = models.CharField(max_length=50, verbose_name="📊 " + _("Skill"))
    level = models.IntegerField(default=50, verbose_name=_("Level"))

    def __str__(self):
        return self.name

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Skills")


class Language(AbstractChildSet, LevelMethodsMixin):
    """
    An object representing the languages that the member holds.
    """

    name = models.CharField(max_length=50, verbose_name="🗣️ " + _("Language"))
    level = models.IntegerField(default=50, verbose_name=_("Level"))

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Language")

    def __str__(self):
        return self.name


class AbstractModelWithDatesAndDescription(auto_prefetch.Model):
    start_date = models.CharField(max_length=16, verbose_name="🗓️ " + _("Start date"))
    end_date = models.CharField(max_length=16, verbose_name="🗓️ " + _("End date"))
    description = models.TextField(
        **null_blank_1024, verbose_name="📝 " + _("What did you learn?")
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

    title = models.CharField(max_length=64, verbose_name="🎓 " + _("Title"))
    institution = models.CharField(max_length=32, verbose_name="🏫 " + _("Institution"))

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Education")


class Experience(AbstractChildSet, AbstractModelWithDatesAndDescription):
    """
    Employment history. See Positions for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position
    """

    title = models.CharField(**null_blank_64, verbose_name="🧑‍💼 " + _("Job title"))
    location = models.CharField(max_length=32, verbose_name="📍 " + _("Location"))
    company = models.CharField(max_length=32, verbose_name="🏢 " + _("Company name"))

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Experience")

    def __str__(self):
        return self.title


class Achievement(AbstractChildSet):
    """Archivement object"""

    title = models.CharField(max_length=64, verbose_name="🏆 " + _("Goal achieved"))
    date = models.CharField(**null_blank_16, verbose_name="🗓️ " + _("Date"))

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Achievements")


class Project(AbstractChildSet):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
    """

    title = models.CharField(
        max_length=64,
        verbose_name="🌍 " + _("Project name"),
    )
    role = models.CharField(
        **null_blank_32,
        verbose_name="🧑‍💼 " + _("Role in the project"),
    )
    organization = models.CharField(
        **null_blank_64,
        verbose_name="🤝 " + _("Organization"),
    )
    link = models.CharField(
        **null_blank_128,
        verbose_name="🔗 " + _("Link"),
    )

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Projects")


class Publication(AbstractChildSet):
    """
    An object representing the various publications associated with the member.
    See Publication Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication
    """

    date = models.CharField(**null_blank_16, verbose_name="🗓️ " + _("Date"))
    title = models.CharField(max_length=128, verbose_name="🔬 " + _("Publication title"))
    publisher = models.CharField(**null_blank_32, verbose_name="📑 " + _("Publisher"))
    link = models.CharField(**null_blank_128, verbose_name="🔗 " + _("Link"))

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Publications")
