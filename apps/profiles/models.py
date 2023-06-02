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


null_blank = {"null": True, "blank": True}
null_blank_16 = {"null": True, "blank": True, "max_length": 16}
null_blank_32 = {"null": True, "blank": True, "max_length": 32}
null_blank_64 = {"null": True, "blank": True, "max_length": 34}
null_blank_128 = {"null": True, "blank": True, "max_length": 128}
null_blank_256 = {"null": True, "blank": True, "max_length": 256}
null_blank_528 = {"null": True, "blank": True, "max_length": 528}
null_blank_1024 = {"null": True, "blank": True, "max_length": 1024}


PROFILE_CATEGORIES = (
    ("temporal", _("Temporal")),
    ("user_profile", _("User profile")),
    ("template", _("Template")),
)


def get_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "profiles/{0}/{1}".format(instance.profile.id, filename)


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

    public = models.BooleanField(default=False)
    slug = models.SlugField(**null_blank_16, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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

        context = {}
        context["profile"] = self
        # one to one children
        for Model, Form in forms.get_forms(singles=True, settings=True).items():
            name = Model._meta.model_name
            context[name + "_form"] = Form(
                instance=getattr(self, name), auto_id="id_%s_" + name
            )
        # one to many children
        for Model, Form in forms.get_forms(inlines=True).items():
            name = Model._meta.model_name
            context[name + "_formset"] = forms.get_inlineformset(Form)(instance=self)

        # photo forms
        context["uploadphoto_form"] = forms.UploadPhotoForm(instance=self.photo)
        context["cropphoto_form"] = forms.CropPhotoForm(instance=self.photo)

        return context

    def build_xml(self):
        # TODO: build xml for the deepl API
        # https://www.deepl.com/docs-api/xml/
        # https://stackoverflow.com/questions/36021526/converting-an-array-dict-to-xml-in-python
        pass


# Abract models and mixins


class ProfileChildMixin:
    def generate_html_id(self):
        return f"{self.__class__.__name__}-{self.id}"

    @property
    def _related_name(self):
        model_name = self.__class__._meta.model_name
        if AbstractChildSet in self.__class__.__bases__:
            return model_name + "_set"
        return model_name

    @property
    def _verbose_name(self):
        return self.__class__._meta.verbose_name

    @property
    def active(self):
        return getattr(self.profile.activationsettings, self._related_name, True)

    @property
    def label(self):
        return getattr(
            self.profile.labelsettings, self._related_name, self._verbose_name
        )


class LevelMethodsMixin:
    @property
    def level_base_5_int(self):
        return (self.level * 5 / 100).__round__()

    @property
    def level_base_6_float(self):
        return self.level * 6 / 100


class AbstractProfileChild(auto_prefetch.Model, ProfileChildMixin):
    profile = auto_prefetch.OneToOneField(Profile, on_delete=models.CASCADE)

    def update_form_url(self):
        cls = self.__class__.__name__
        return reverse("profiles:update-form", kwargs={"klass": cls, "id": self.id})

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


class AbstractChildSet(auto_prefetch.Model, ProfileChildMixin):
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    order = models.PositiveSmallIntegerField(default=1)

    def get_delete_url(self):
        cls = self.__class__.__name__
        return reverse("profiles:delete-child", kwargs={"klass": cls, "id": self.id})

    def save(self, *args, **kwargs):
        if not self.pk:
            last = self.__class__.objects.filter(profile=self.profile).last()
            self.order = last.order + 1 if last else 1

        super().save(*args, **kwargs)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ("order",)


class AbstractProfileSetting(auto_prefetch.Model):
    profile = auto_prefetch.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="%(class)s"
    )

    def update_settings_url(self):
        cls = self.__class__.__name__
        return reverse("profiles:update-settings", kwargs={"klass": cls, "id": self.id})

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


# Profile settings models


class ActivationSettings(AbstractProfileSetting):
    photo = models.BooleanField(default=True)
    jobtitle = models.BooleanField(default=True)
    website = models.BooleanField(default=True)
    description = models.BooleanField(default=True)
    skill_set = models.BooleanField(default=True)
    language_set = models.BooleanField(default=False)
    education_set = models.BooleanField(default=True)
    experience_set = models.BooleanField(default=True)
    achievement_set = models.BooleanField(default=False)
    project_set = models.BooleanField(default=False)
    publication_set = models.BooleanField(default=False)


class LabelSettings(AbstractProfileSetting):
    website = models.CharField(max_length=32, default=_("Website"))
    skill_set = models.CharField(max_length=32, default=_("Skills"))
    description = models.CharField(max_length=32, default=_("Description"))
    skill_set = models.CharField(max_length=32, default=_("Skills"))
    language_set = models.CharField(max_length=32, default=_("Languages"))
    education_set = models.CharField(max_length=32, default=_("Education"))
    experience_set = models.CharField(max_length=32, default=_("Work experience"))
    achievement_set = models.CharField(max_length=32, default=_("Achievements"))
    project_set = models.CharField(max_length=32, default=_("Projects"))
    publication_set = models.CharField(max_length=32, default=_("Publications"))


class Photo(AbstractProfileChild):
    full = models.ImageField(null=True, upload_to=get_upload_path)
    cropped = models.ImageField(null=True, upload_to=get_upload_path)
    crop_x = models.PositiveSmallIntegerField(**null_blank)
    crop_y = models.PositiveSmallIntegerField(**null_blank)
    crop_width = models.PositiveSmallIntegerField(**null_blank)
    crop_height = models.PositiveSmallIntegerField(**null_blank)

    def upload_url(self):
        return reverse("profiles:upload-photo", kwargs={"id": self.id})

    def crop_url(self):
        return reverse("profiles:crop-photo", kwargs={"id": self.id})

    def delete_url(self):
        return reverse("profiles:delete-photo-files", kwargs={"id": self.id})

    def crop(self):
        if self.full:
            self.cropped.save(
                "cropped_" + self.full.name.split("/")[-1],
                ContentFile(self.full.read()),
            )
            image = Image.open(self.cropped)
            cropping_area = (
                self.crop_x,
                self.crop_y,
                self.crop_x + self.crop_width,
                self.crop_y + self.crop_height,
            )
            cropped_image = image.crop(cropping_area)
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(self.cropped.path)
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.full:
            size_modified = False
            try:
                img = Image.open(self.full)
            except Exception as e:
                raise e

            if img.height > 1200 or img.width > 1200:
                new_size = (1200, 1200)
                img.thumbnail(new_size)
                img.save(self.full.path)
                size_modified = True

            if not self.cropped:
                if size_modified:
                    img = Image.open(self.full)
                distance = int(0.95 * min([img.height, img.width]))
                self.crop_width, self.crop_height = distance, distance
                self.crop_x = int((img.width - distance) / 2)
                self.crop_y = int((img.height - distance) / 2)
                super().save(*args, **kwargs)


class Description(AbstractProfileChild):
    text = models.TextField()
    rows = models.PositiveSmallIntegerField(default=15)

    def save(self, *args, **kwargs):
        rows = int(len(self.text) / 35)
        self.rows = rows if rows > 3 else 3
        super().save(*args, **kwargs)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Description")


class Fullname(AbstractProfileChild):
    text = models.CharField(verbose_name=_("Full name"), **null_blank_32)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Full name")


class Jobtitle(AbstractProfileChild):
    text = models.CharField(verbose_name=_("Job title"), **null_blank_16)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Job title")


class Location(AbstractProfileChild):
    text = models.CharField(verbose_name=_("Location"), **null_blank_16)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Location")


class Birth(AbstractProfileChild):
    text = models.CharField(verbose_name=_("Date of birth"), **null_blank_16)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Date of birth")


class Phone(AbstractProfileChild):
    text = models.CharField(verbose_name=_("Phone number"), **null_blank_16)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Phone number")


class Email(AbstractProfileChild):
    text = models.CharField(verbose_name=_("Email"), **null_blank_32)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Email")


class Website(AbstractProfileChild):
    text = models.CharField(verbose_name=_("Website"), **null_blank_32)

    class Meta(AbstractProfileChild.Meta):
        verbose_name = _("Website")


class Skill(AbstractChildSet, LevelMethodsMixin):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=50)

    def __str__(self):
        return self.name

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Skills")


class Language(AbstractChildSet, LevelMethodsMixin):
    """
    An object representing the languages that the member holds.
    """

    name = models.CharField(max_length=50)
    level = models.IntegerField(default=3)

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Language")

    def __str__(self):
        return self.name


class DatesAndDescriptionFields(auto_prefetch.Model):
    start_date = models.CharField(**null_blank_16, verbose_name=_("🗓️ Start"))
    end_date = models.CharField(**null_blank_16, verbose_name=_("🗓️ End"))
    description = models.TextField(**null_blank_1024, verbose_name=_("📝 Description"))
    rows = models.PositiveSmallIntegerField(default=10)

    def save(self, *args, **kwargs):
        rows = int(len(self.description) / 80)
        self.rows = rows if rows > 3 else 3
        super().save(*args, **kwargs)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


class Education(AbstractChildSet, DatesAndDescriptionFields):
    """
    An object representing the member's educational background.
    See Education Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/education
    """

    title = models.CharField(**null_blank_64, verbose_name=_("🎓 Title"))
    institution = models.CharField(**null_blank_64, verbose_name=_("🏫 Institution"))

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Education")


class Experience(AbstractChildSet, DatesAndDescriptionFields):
    """
    Employment history. See Positions for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position
    """

    title = models.CharField(**null_blank_64, verbose_name=_("🎓 Title"))
    location = models.CharField(**null_blank_16)
    company = models.CharField(**null_blank_16)

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Experience")

    def __str__(self):
        return self.title


class Achievement(AbstractChildSet):
    """Archivement object"""

    title = models.CharField(**null_blank_128, verbose_name=_("🎓 Title"))
    date = models.CharField(**null_blank_16, verbose_name=_("🗓️ Date"))
    link = models.CharField(**null_blank_128)

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Achievements")


class Project(AbstractChildSet):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
    """

    title = models.CharField(**null_blank_64)
    role = models.CharField(**null_blank_32)
    organization = models.CharField(**null_blank_64)
    link = models.CharField(**null_blank_128)
    description = models.TextField(**null_blank_1024)

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Projects")


class Publication(AbstractChildSet):
    """
    An object representing the various publications associated with the member.
    See Publication Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication
    """

    title = models.CharField(null=True, blank=True, max_length=200)
    issuing_date = models.CharField(null=True, blank=True, max_length=20)
    authors = models.CharField(null=True, blank=True, max_length=200)
    publisher = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta(AbstractChildSet.Meta):
        verbose_name = _("Publications")
