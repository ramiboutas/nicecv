import uuid

import auto_prefetch
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


def photo_path(instance):
    # file will be uploaded to MEDIA_ROOT
    return "profiles/photos/{0}".format(instance.profile.id)


def manage_instance_ordering(self):
    """
    This function manages the ordering of an instance when it is created
    new_instance.order > max_order_of_objects + 1
    """
    if self._state.adding:
        try:
            current_maximum_order = self.__class__.objects.latest("order").order
            self.order = current_maximum_order + 1
        except:
            pass  # exception if objects do not exist


null_blank = {"null": True, "blank": True}
null_blank_16 = {"null": True, "blank": True, "max_length": 16}
null_blank_32 = {"null": True, "blank": True, "max_length": 32}
null_blank_64 = {"null": True, "blank": True, "max_length": 34}
null_blank_128 = {"null": True, "blank": True, "max_length": 128}


class Profile(auto_prefetch.Model):
    """
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="profile_set",
        **null_blank,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # name
    fullname = models.CharField(verbose_name=_("Full name"), **null_blank_32)
    jobtitle = models.CharField(verbose_name=_("Job title"), **null_blank_32)
    location = models.CharField(verbose_name=_("Location"), **null_blank_32)
    birth = models.CharField(verbose_name=_("Date of birth"), **null_blank_16)
    phone = models.CharField(verbose_name=_("Phone number"), **null_blank_16)
    email = models.CharField(verbose_name=_("Email address"), **null_blank_32)
    website = models.CharField(verbose_name=_("Website"), **null_blank_32)

    def __str__(self):
        return f"{self.fullname} {self.email}"

    # profile object
    @property
    def update_url(self):
        return reverse("profiles:update", kwargs={"id": self.id})

    @property
    def update_fields_url(self):
        return reverse("profiles:update-fields", kwargs={"id": self.id})

    def delete_object_url(self):
        return reverse("profiles:delete", kwargs={"id": self.id})

    # update any profile field
    def update_field(self, field_name, field_value):
        setattr(self, field_name, field_value)
        self.save()

    def save(self, *args, **kwargs):
        if self._state.adding:
            pass

        super().save(*args, **kwargs)


class Photo(auto_prefetch.Model):
    profile = auto_prefetch.OneToOneField(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    full = models.ImageField(null=True, blank=True, upload_to=photo_path)
    cropped = models.ImageField(null=True, blank=True, upload_to=photo_path)
    crop_x = models.PositiveSmallIntegerField(null=True, blank=True)
    crop_y = models.PositiveSmallIntegerField(null=True, blank=True)
    crop_width = models.PositiveSmallIntegerField(null=True, blank=True)
    crop_height = models.PositiveSmallIntegerField(null=True, blank=True)

    def upload_photo_url(self):
        return reverse("profiles:photo-upload", kwargs={"pk": self.pk})

    def crop_photo_url(self):
        return reverse("profiles:photo-crop", kwargs={"pk": self.pk})

    def save_cropping_points(self, crop_x, crop_y, crop_width, crop_height):
        self.crop_x = crop_x
        self.crop_y = crop_y
        self.crop_width = crop_width
        self.crop_height = crop_height
        self.save()

    def crop_photo(self, crop_x, crop_y, crop_width, crop_height):
        if self.full:
            photo_full_copy = ContentFile(self.full.read())
            cropped_name = "cropped_" + self.full.name.split("/")[-1]
            self.cropped.save(cropped_name, photo_full_copy)
            image = Image.open(self.cropped)
            cropping_area = (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height)
            cropped_image = image.crop(cropping_area)
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(self.photo.path)
            self.save_cropping_points(crop_x, crop_y, crop_width, crop_height)
            return self

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.full is not None:
            try:
                img = Image.open(self.full)
                if img.height > 1200 or img.width > 1200:
                    # image proportion is manteined
                    new_size = (1200, 1200)
                    img.thumbnail(new_size)
                    img.save(self.full.path)
            except:
                pass


# class FirstName(auto_prefetch.Model):
#     profile = models.OneToOneField(Profile, verbose_name=_(""), on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     active = models.BooleanField(default=True)


class AbstractChild(auto_prefetch.Model):
    profile = auto_prefetch.OneToOneField(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


class Description(AbstractChild):
    label = models.CharField(max_length=32, default=_("About me"))
    text = models.TextField()


class SkillSet(AbstractChild):
    """
    An object representing the skills that the member holds.
    See Skill Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/skill
    """

    label = models.CharField(max_length=100, default=_("Skills"))

    class Meta(auto_prefetch.Model.Meta):
        default_related_name = "skill_set"


class SkillItem(auto_prefetch.Model):
    skill_set = auto_prefetch.ForeignKey(SkillSet, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=50)  # Linkedin does not include this

    def __str__(self):
        return self.name

    @property
    def level_base_5_int(self):
        return (self.level * 5 / 100).__round__()

    @property
    def level_base_6_float(self):
        return self.level * 6 / 100

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("-level",)
        default_related_name = "items"


# class Language(auto_prefetch.Model):
#     """
#     An object representing the languages that the member holds.
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="language_set"
#     )
#     name = models.CharField(max_length=50)
#     level = models.IntegerField(default=3)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "id",
#             "level",
#         )

#     def __str__(self):
#         return self.name

#     @property
#     def level_base_5_int(self):
#         return (self.level * 5 / 100).__round__()

#     @property
#     def level_base_6_float(self):
#         return self.level * 6 / 100

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE,
#             },
#         )


# class Education(auto_prefetch.Model):
#     """
#     An object representing the member's educational background.
#     See Education Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/education
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="education_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     grade = models.CharField(null=True, blank=True, max_length=20)
#     institution = models.CharField(null=True, blank=True, max_length=100)
#     institution_link = models.CharField(null=True, blank=True, max_length=200)
#     start_date = models.CharField(null=True, blank=True, max_length=50)
#     end_date = models.CharField(null=True, blank=True, max_length=50)
#     description = models.TextField(null=True, blank=True, max_length=300)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def __str__(self):
#         return self.title

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Experience(auto_prefetch.Model):
#     """
#     Employment history. See Positions for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="experience_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     location = models.CharField(null=True, blank=True, max_length=100)
#     company = models.CharField(null=True, blank=True, max_length=100)
#     company_link = models.CharField(null=True, blank=True, max_length=100)
#     start_date = models.CharField(null=True, blank=True, max_length=100)
#     end_date = models.CharField(null=True, blank=True, max_length=100)
#     description = models.TextField(null=True, blank=True, max_length=1000)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def __str__(self):
#         return self.title

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Certification(auto_prefetch.Model):
#     """
#     An object representing the certifications that the member holds.
#     See Certification Fields for a description of the fields available within this object.
#     https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/certification
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, related_name="certification_set", on_delete=models.CASCADE
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     issuing_date = models.CharField(null=True, blank=True, max_length=100)
#     issuer = models.CharField(null=True, blank=True, max_length=100)
#     link = models.CharField(null=True, blank=True, max_length=100)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Course(auto_prefetch.Model):
#     """
#     An object representing courses the member has taken.
#     See Course Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/course
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, related_name="course_set", on_delete=models.CASCADE
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     issuing_date = models.CharField(null=True, blank=True, max_length=100)
#     issuer = models.CharField(null=True, blank=True, max_length=100)
#     hours = models.CharField(null=True, blank=True, max_length=100)
#     link = models.CharField(null=True, blank=True, max_length=100)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Honor(auto_prefetch.Model):
#     """
#     An object representing the various honors and awards the member has received.
#     See Honor Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/honor
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="honor_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     issuing_date = models.CharField(null=True, blank=True, max_length=100)
#     issuer = models.CharField(null=True, blank=True, max_length=100)
#     link = models.CharField(null=True, blank=True, max_length=100)
#     # description = models.TextField(null=True, blank=True)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Organization(auto_prefetch.Model):
#     """
#     An object representing the organizations that the member is in.
#     See Organization Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/organization
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="organization_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     role = models.CharField(null=True, blank=True, max_length=100)
#     organization = models.CharField(null=True, blank=True, max_length=100)
#     organization_link = models.CharField(null=True, blank=True, max_length=100)
#     start_date = models.CharField(null=True, blank=True, max_length=50)
#     end_date = models.CharField(null=True, blank=True, max_length=50)
#     description = models.TextField(null=True, blank=True)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Patent(auto_prefetch.Model):
#     """
#     An object representing the various patents associated with the member.
#     See Patent Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/patent
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="patent_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     number = models.CharField(null=True, blank=True, max_length=15)
#     issuer = models.CharField(null=True, blank=True, max_length=100)
#     issuing_date = models.CharField(
#         null=True, blank=True, max_length=100
#     )  # when pending = False
#     inventors = models.CharField(null=True, blank=True, max_length=200)
#     link = models.CharField(null=True, blank=True, max_length=100)
#     description = models.TextField(
#         null=True, blank=True
#     )  # suggest to use to include if the patent is patent is pending and more relevant info

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Project(auto_prefetch.Model):
#     """
#     An object representing the various projects associated with the member.
#     See Project Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="project_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     role = models.CharField(null=True, blank=True, max_length=100)
#     start_date = models.CharField(null=True, blank=True, max_length=100)
#     end_date = models.CharField(null=True, blank=True, max_length=100)
#     organization = models.CharField(null=True, blank=True, max_length=100)
#     link = models.CharField(null=True, blank=True, max_length=100)
#     description = models.TextField(null=True, blank=True)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
#             },
#         )

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Publication(auto_prefetch.Model):
#     """
#     An object representing the various publications associated with the member.
#     See Publication Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="publication_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=200)
#     issuing_date = models.CharField(null=True, blank=True, max_length=20)
#     authors = models.CharField(null=True, blank=True, max_length=200)
#     publisher = models.CharField(null=True, blank=True, max_length=100)
#     link = models.CharField(null=True, blank=True, max_length=100)
#     description = models.TextField(null=True, blank=True, max_length=1000)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
#             },
#         )

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# class Volunteering(auto_prefetch.Model):
#     """
#     An object representing the member's volunteering experience.
#     See Volunteering Experience Fields for a description of the fields available within this object.
#     # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/volunteering-experience
#     """

#     profile = auto_prefetch.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name="volunteering_set"
#     )
#     order = models.SmallIntegerField(default=0)

#     title = models.CharField(null=True, blank=True, max_length=100)
#     location = models.CharField(null=True, blank=True, max_length=100)
#     organization = models.CharField(null=True, blank=True, max_length=100)
#     organization_link = models.CharField(null=True, blank=True, max_length=100)
#     start_date = models.CharField(null=True, blank=True, max_length=100)
#     end_date = models.CharField(null=True, blank=True, max_length=100)
#     description = models.TextField(null=True, blank=True, max_length=1000)

#     class Meta(auto_prefetch.Model.Meta):
#         ordering = (
#             "order",
#             "id",
#         )

#     def update_object_url(self):
#         return reverse(
#             "profiles_update_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
#             },
#         )

#     def delete_object_url(self):
#         return reverse(
#             "profiles_delete_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
#             },
#         )

#     def move_up_object_url(self):
#         return reverse(
#             "profiles_move_up_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
#             },
#         )

#     def move_down_object_url(self):
#         return reverse(
#             "profiles_move_down_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
#             },
#         )

#     def copy_object_url(self):
#         return reverse(
#             "profiles_copy_child_object",
#             kwargs={
#                 "pk": self.pk,
#                 "pk_parent": self.profile.pk,
#                 "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
#             },
#         )

#     def save(self, *args, **kwargs):
#         manage_instance_ordering(self)
#         super().save(*args, **kwargs)


# def get_child_class(slug):
#     if slug == SLUG_FOR_CHILD_OBJECT_SKILL:
#         return Skill

#     if slug == SLUG_FOR_CHILD_OBJECT_LANGUAGE:
#         return Language

#     if slug == SLUG_FOR_CHILD_OBJECT_EDUCATION:
#         return Education

#     if slug == SLUG_FOR_CHILD_OBJECT_EXPERIENCE:
#         return Experience

#     if slug == SLUG_FOR_CHILD_OBJECT_CERTIFICATION:
#         return Certification

#     if slug == SLUG_FOR_CHILD_OBJECT_COURSE:
#         return Course

#     if slug == SLUG_FOR_CHILD_OBJECT_HONOR:
#         return Honor

#     if slug == SLUG_FOR_CHILD_OBJECT_ORGANIZATION:
#         return Organization

#     if slug == SLUG_FOR_CHILD_OBJECT_PATENT:
#         return Patent

#     if slug == SLUG_FOR_CHILD_OBJECT_PROJECT:
#         return Project

#     if slug == SLUG_FOR_CHILD_OBJECT_PUBLICATION:
#         return Publication

#     if slug == SLUG_FOR_CHILD_OBJECT_VOLUNTEERING:
#         return Volunteering


# def update_child_object(slug=None, child_object=None, request=None):
#     if slug == SLUG_FOR_CHILD_OBJECT_SKILL:
#         child_object.name = request.POST.get("name")
#         child_object.level = request.POST.get("level")

#     if slug == SLUG_FOR_CHILD_OBJECT_LANGUAGE:
#         child_object.name = request.POST.get("name")
#         child_object.level = request.POST.get("level")

#     if slug == SLUG_FOR_CHILD_OBJECT_EDUCATION:  # education
#         child_object.title = request.POST.get("title")
#         child_object.grade = request.POST.get("grade")
#         child_object.start_date = request.POST.get("start_date")
#         child_object.end_date = request.POST.get("end_date")
#         child_object.institution = request.POST.get("institution")
#         child_object.institution_link = request.POST.get("institution_link")
#         child_object.description = request.POST.get("description")

#     if slug == SLUG_FOR_CHILD_OBJECT_EXPERIENCE:
#         child_object.title = request.POST.get("title")
#         child_object.location = request.POST.get("location")
#         child_object.company = request.POST.get("company")
#         child_object.company_link = request.POST.get("company_link")
#         child_object.start_date = request.POST.get("start_date")
#         child_object.end_date = request.POST.get("end_date")
#         child_object.description = request.POST.get("description")

#     if slug == SLUG_FOR_CHILD_OBJECT_CERTIFICATION:
#         child_object.title = request.POST.get("title")
#         child_object.issuing_date = request.POST.get("issuing_date")
#         child_object.issuer = request.POST.get("issuer")
#         child_object.link = request.POST.get("link")

#     if slug == SLUG_FOR_CHILD_OBJECT_COURSE:
#         child_object.title = request.POST.get("title")
#         child_object.issuing_date = request.POST.get("issuing_date")
#         child_object.issuer = request.POST.get("issuer")
#         child_object.hours = request.POST.get("hours")
#         child_object.link = request.POST.get("link")

#     if slug == SLUG_FOR_CHILD_OBJECT_HONOR:
#         child_object.title = request.POST.get("title")
#         child_object.issuing_date = request.POST.get("issuing_date")
#         child_object.issuer = request.POST.get("issuer")
#         child_object.link = request.POST.get("link")

#     if slug == SLUG_FOR_CHILD_OBJECT_ORGANIZATION:
#         child_object.role = request.POST.get("role")
#         child_object.organization = request.POST.get("organization")
#         child_object.organization_link = request.POST.get("organization_link")
#         child_object.start_date = request.POST.get("start_date")
#         child_object.end_date = request.POST.get("end_date")
#         child_object.description = request.POST.get("description")

#     if slug == SLUG_FOR_CHILD_OBJECT_PATENT:
#         child_object.title = request.POST.get("title")
#         child_object.number = request.POST.get("number")
#         child_object.issuer = request.POST.get("issuer")
#         child_object.issuing_date = request.POST.get("issuing_date")
#         child_object.inventors = request.POST.get("inventors")
#         child_object.link = request.POST.get("link")
#         child_object.description = request.POST.get("description")

#     if slug == SLUG_FOR_CHILD_OBJECT_PROJECT:
#         child_object.title = request.POST.get("title")
#         child_object.role = request.POST.get("role")
#         child_object.start_date = request.POST.get("start_date")
#         child_object.end_date = request.POST.get("end_date")
#         child_object.organization = request.POST.get("organization")
#         child_object.link = request.POST.get("link")
#         child_object.description = request.POST.get("description")

#     if slug == SLUG_FOR_CHILD_OBJECT_PUBLICATION:
#         child_object.title = request.POST.get("title")
#         child_object.issuing_date = request.POST.get("issuing_date")
#         child_object.authors = request.POST.get("authors")
#         child_object.publisher = request.POST.get("publisher")
#         child_object.link = request.POST.get("link")
#         child_object.description = request.POST.get("description")

#     if slug == SLUG_FOR_CHILD_OBJECT_VOLUNTEERING:
#         child_object.title = request.POST.get("title")
#         child_object.location = request.POST.get("location")
#         child_object.organization = request.POST.get("organization")
#         child_object.organization_link = request.POST.get("organization_link")
#         child_object.start_date = request.POST.get("start_date")
#         child_object.end_date = request.POST.get("end_date")
#         child_object.description = request.POST.get("description")

#     child_object.save()


# def set_activation_state(slug=None, object=None, active=True):
#     if slug == SLUG_FOR_PROFILE_FIELD_FIRSTNAME:
#         object.firstname_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_LASTNAME:
#         object.lastname_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_JOBTITLE:
#         object.jobtitle_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_LOCATION:
#         object.location_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_BIRTH:
#         object.birth_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_PHONE:
#         object.phone_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_EMAIL:
#         object.email_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_DESCRIPTION:
#         object.description_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_WEBSITE:
#         object.website_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_LINKEDIN:
#         object.linkedin_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_SKYPE:
#         object.skype_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_INSTAGRAM:
#         object.instagram_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_TWITTER:
#         object.twitter_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_FACEBOOK:
#         object.facebook_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_YOUTUBE:
#         object.youtube_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_GITHUB:
#         object.github_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_GITLAB:
#         object.gitlab_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW:
#         object.stackoverflow_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_MEDIUM:
#         object.medium_active = active

#     if slug == SLUG_FOR_PROFILE_FIELD_ORCID:
#         object.orcid_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_SKILL:
#         object.skill_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_LANGUAGE:
#         object.language_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_EDUCATION:
#         object.education_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_EXPERIENCE:
#         object.experience_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_CERTIFICATION:
#         object.certification_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_COURSE:
#         object.course_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_HONOR:
#         object.honor_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_ORGANIZATION:
#         object.organization_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_PATENT:
#         object.patent_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_PROJECT:
#         object.project_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_PUBLICATION:
#         object.publication_active = active

#     if slug == SLUG_FOR_CHILD_OBJECT_VOLUNTEERING:
#         object.volunteering_active = active

#     object.save()


# def get_child_object(slug=None, pk=None, profile=None):
#     """
#     This function gets an instance object
#     """
#     Klass = get_child_class(slug)
#     return get_object_or_404(Klass, profile=profile, pk=pk)


# def create_empty_child_object(slug=None, profile=None):
#     """
#     This function creates an empty object associated with a profile instance
#     """
#     Klass = get_child_class(slug)
#     return Klass(profile=profile)


# def get_above_child_object(slug=None, child_object=None, profile=None):
#     """
#     This function gets an instance object that is located before the "child_object"
#     """
#     Klass = get_child_class(slug)
#     return Klass.objects.filter(order__lt=child_object.order, profile=profile).last()


# def get_below_child_object(slug=None, child_object=None, profile=None):
#     """
#     This function gets an instance object that is located after the "child_object"
#     """
#     Klass = get_child_class(slug)
#     return Klass.objects.filter(order__gt=child_object.order, profile=profile).first()


# ####################################################################################

# from apps.tex.models import ResumeTemplate


# class Resume(auto_prefetch.Model):
#     profile = auto_prefetch.ForeignKey(
#         Profile, null=True, related_name="resume_set", on_delete=models.SET_NULL
#     )
#     template = auto_prefetch.ForeignKey(
#         ResumeTemplate, null=True, on_delete=models.SET_NULL
#     )
#     image = models.ImageField(null=True, upload_to="resumes/images")
#     pdf = models.FileField(null=True, upload_to="resumes/pdfs")

#     def download_resume_pdf_url(self):
#         return reverse(
#             "profiles_get_resume_pdf",
#             kwargs={"pk": self.pk, "pk_parent": self.profile.pk},
#         )

#     def download_resume_image_url(self):
#         return reverse(
#             "profiles_get_resume_image",
#             kwargs={"pk": self.pk, "pk_parent": self.profile.pk},
#         )
