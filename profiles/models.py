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


# slugs. Used in urls (slug) & in templates  (profiles/partials/slug/file.html)
SLUG_FOR_PROFILE_FIELD_FIRSTNAME = "firstname"
SLUG_FOR_PROFILE_FIELD_LASTNAME = "lastname"
SLUG_FOR_PROFILE_FIELD_JOBTITLE = "jobtitle"
SLUG_FOR_PROFILE_FIELD_LOCATION = "location"
SLUG_FOR_PROFILE_FIELD_BIRTH = "birth"
SLUG_FOR_PROFILE_FIELD_PHONE = "phone"
SLUG_FOR_PROFILE_FIELD_EMAIL = "email"
SLUG_FOR_PROFILE_FIELD_DESCRIPTION = "description"
SLUG_FOR_PROFILE_FIELD_WEBSITE = "website"
SLUG_FOR_PROFILE_FIELD_LINKEDIN = "linkedin"
SLUG_FOR_PROFILE_FIELD_SKYPE = "skype"
SLUG_FOR_PROFILE_FIELD_INSTAGRAM = "instagram"
SLUG_FOR_PROFILE_FIELD_TWITTER = "twitter"
SLUG_FOR_PROFILE_FIELD_FACEBOOK = "facebook"
SLUG_FOR_PROFILE_FIELD_YOUTUBE = "youtube"
SLUG_FOR_PROFILE_FIELD_GITHUB = "github"
SLUG_FOR_PROFILE_FIELD_GITLAB = "gitlab"
SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW = "stackoverflow"
SLUG_FOR_PROFILE_FIELD_MEDIUM = "medium"
SLUG_FOR_PROFILE_FIELD_ORCID = "orcid"
SLUG_FOR_PROFILE_FIELD_DESCRIPTION_LABEL = "description-label"


SLUG_FOR_CHILD_OBJECT_SKILL = "skill"
SLUG_FOR_CHILD_OBJECT_LANGUAGE = "language"
SLUG_FOR_CHILD_OBJECT_EDUCATION = "education"
SLUG_FOR_CHILD_OBJECT_EXPERIENCE = "experience"
SLUG_FOR_CHILD_OBJECT_CERTIFICATION = "certification"
SLUG_FOR_CHILD_OBJECT_COURSE = "course"
SLUG_FOR_CHILD_OBJECT_HONOR = "honor"
SLUG_FOR_CHILD_OBJECT_ORGANIZATION = "organization"
SLUG_FOR_CHILD_OBJECT_PATENT = "patent"
SLUG_FOR_CHILD_OBJECT_PROJECT = "project"
SLUG_FOR_CHILD_OBJECT_PUBLICATION = "publication"
SLUG_FOR_CHILD_OBJECT_VOLUNTEERING = "volunteering"


SLUG_FOR_CHILD_OBJECT_SKILL_LABEL = "skill-label"
SLUG_FOR_CHILD_OBJECT_LANGUAGE_LABEL = "language-label"
SLUG_FOR_CHILD_OBJECT_EDUCATION_LABEL = "education-label"
SLUG_FOR_CHILD_OBJECT_EXPERIENCE_LABEL = "experience-label"
SLUG_FOR_CHILD_OBJECT_CERTIFICATION_LABEL = "certification-label"
SLUG_FOR_CHILD_OBJECT_COURSE_LABEL = "course-label"
SLUG_FOR_CHILD_OBJECT_HONOR_LABEL = "honor-label"
SLUG_FOR_CHILD_OBJECT_ORGANIZATION_LABEL = "organization-label"
SLUG_FOR_CHILD_OBJECT_PATENT_LABEL = "patent-label"
SLUG_FOR_CHILD_OBJECT_PROJECT_LABEL = "project-label"
SLUG_FOR_CHILD_OBJECT_PUBLICATION_LABEL = "publication-label"
SLUG_FOR_CHILD_OBJECT_VOLUNTEERING_LABEL = "volunteering-label"


PROFILE_FIELD_MAPPING = {
    SLUG_FOR_PROFILE_FIELD_FIRSTNAME: "firstname",
    SLUG_FOR_PROFILE_FIELD_LASTNAME: "lastname",
    SLUG_FOR_PROFILE_FIELD_JOBTITLE: "jobtitle",
    SLUG_FOR_PROFILE_FIELD_LOCATION: "location",
    SLUG_FOR_PROFILE_FIELD_BIRTH: "birth",
    SLUG_FOR_PROFILE_FIELD_PHONE: "phone",
    SLUG_FOR_PROFILE_FIELD_EMAIL: "email",
    SLUG_FOR_PROFILE_FIELD_DESCRIPTION: "description",
    SLUG_FOR_PROFILE_FIELD_WEBSITE: "website",
    SLUG_FOR_PROFILE_FIELD_LINKEDIN: "linkedin",
    SLUG_FOR_PROFILE_FIELD_SKYPE: "skype",
    SLUG_FOR_PROFILE_FIELD_INSTAGRAM: "instagram",
    SLUG_FOR_PROFILE_FIELD_TWITTER: "twitter",
    SLUG_FOR_PROFILE_FIELD_FACEBOOK: "facebook",
    SLUG_FOR_PROFILE_FIELD_YOUTUBE: "youtube",
    SLUG_FOR_PROFILE_FIELD_GITHUB: "github",
    SLUG_FOR_PROFILE_FIELD_GITLAB: "gitlab",
    SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW: "stackoverflow",
    SLUG_FOR_PROFILE_FIELD_MEDIUM: "medium",
    SLUG_FOR_PROFILE_FIELD_ORCID: "orcid",
    SLUG_FOR_PROFILE_FIELD_DESCRIPTION_LABEL: "description-label",
    SLUG_FOR_CHILD_OBJECT_SKILL_LABEL: "skill_label",
    SLUG_FOR_CHILD_OBJECT_LANGUAGE_LABEL: "language_label",
    SLUG_FOR_CHILD_OBJECT_EDUCATION_LABEL: "education_label",
    SLUG_FOR_CHILD_OBJECT_EXPERIENCE_LABEL: "experience_label",
    SLUG_FOR_CHILD_OBJECT_CERTIFICATION_LABEL: "certification_label",
    SLUG_FOR_CHILD_OBJECT_COURSE_LABEL: "course_label",
    SLUG_FOR_CHILD_OBJECT_HONOR_LABEL: "honor_label",
    SLUG_FOR_CHILD_OBJECT_ORGANIZATION_LABEL: "organization_label",
    SLUG_FOR_CHILD_OBJECT_PATENT_LABEL: "patent_label",
    SLUG_FOR_CHILD_OBJECT_PROJECT_LABEL: "project_label",
    SLUG_FOR_CHILD_OBJECT_PUBLICATION_LABEL: "publication_label",
    SLUG_FOR_CHILD_OBJECT_VOLUNTEERING_LABEL: "volunteering_label",
}


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


class Profile(auto_prefetch.Model):
    """
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="profile_set",
        null=True,
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    task_id = models.CharField(null=True, blank=True, max_length=50)

    # media
    photo = models.ImageField(
        null=True, blank=True, upload_to="profiles/cropped_photos/"
    )
    photo_full = models.ImageField(
        null=True, blank=True, upload_to="profiles/full_photos/"
    )

    # name
    firstname = models.CharField(null=True, blank=True, max_length=50)
    lastname = models.CharField(null=True, blank=True, max_length=50)
    jobtitle = models.CharField(max_length=50)
    location = models.CharField(null=True, blank=True, max_length=50)
    birth = models.CharField(null=True, blank=True, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=50)
    email = models.CharField(null=True, blank=True, max_length=50)
    website = models.CharField(null=True, blank=True, max_length=50)
    linkedin = models.CharField(null=True, blank=True, max_length=50)
    skype = models.CharField(null=True, blank=True, max_length=50)
    instagram = models.CharField(null=True, blank=True, max_length=50)
    twitter = models.CharField(null=True, blank=True, max_length=50)
    facebook = models.CharField(null=True, blank=True, max_length=50)
    youtube = models.CharField(null=True, blank=True, max_length=50)
    github = models.CharField(null=True, blank=True, max_length=50)
    gitlab = models.CharField(null=True, blank=True, max_length=50)
    stackoverflow = models.CharField(null=True, blank=True, max_length=50)
    medium = models.CharField(null=True, blank=True, max_length=50)
    orcid = models.CharField(null=True, blank=True, max_length=50)

    # description & interests
    description = models.TextField(null=True, blank=True, max_length=1000)
    interests = models.CharField(null=True, blank=True, max_length=200)

    # activation of fields
    jobtitle_active = models.BooleanField(default=True)
    location_active = models.BooleanField(default=True)
    birth_active = models.BooleanField(default=True)
    phone_active = models.BooleanField(default=True)
    email_active = models.BooleanField(default=True)
    description_active = models.BooleanField(default=True)
    website_active = models.BooleanField(default=False)
    linkedin_active = models.BooleanField(default=True)
    skype_active = models.BooleanField(default=True)
    instagram_active = models.BooleanField(default=False)
    twitter_active = models.BooleanField(default=False)
    facebook_active = models.BooleanField(default=False)
    youtube_active = models.BooleanField(default=False)
    github_active = models.BooleanField(default=False)
    gitlab_active = models.BooleanField(default=False)
    stackoverflow_active = models.BooleanField(default=False)
    medium_active = models.BooleanField(default=False)
    orcid_active = models.BooleanField(default=False)

    # activation of child objects
    skill_active = models.BooleanField(default=True)
    language_active = models.BooleanField(default=True)
    education_active = models.BooleanField(default=True)
    experience_active = models.BooleanField(default=True)
    certification_active = models.BooleanField(default=False)
    course_active = models.BooleanField(default=True)
    honor_active = models.BooleanField(default=False)
    organization_active = models.BooleanField(default=False)
    patent_active = models.BooleanField(default=False)
    project_active = models.BooleanField(default=False)
    publication_active = models.BooleanField(default=False)
    volunteering_active = models.BooleanField(default=False)

    # labels
    description_label = models.CharField(max_length=100, default=_("About me"))
    skill_label = models.CharField(max_length=100, default=_("Skills"))
    language_label = models.CharField(max_length=100, default=_("Languages"))
    education_label = models.CharField(max_length=100, default=_("Education"))
    experience_label = models.CharField(max_length=100, default=_("Work experience"))
    certification_label = models.CharField(max_length=100, default=_("Certifications"))
    course_label = models.CharField(max_length=100, default=_("Courses"))
    honor_label = models.CharField(max_length=100, default=_("Honors and Awards"))
    organization_label = models.CharField(max_length=100, default=_("Organizations"))
    patent_label = models.CharField(max_length=100, default=_("Patents"))
    project_label = models.CharField(max_length=100, default=_("Projects"))
    publication_label = models.CharField(max_length=100, default=_("Publications"))
    volunteering_label = models.CharField(
        max_length=100, default=_("Volunteering work")
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.email}"

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    # profile object
    def get_update_url(self):
        return reverse("profiles_update", kwargs={"pk": self.pk})

    def delete_object_url(self):
        return reverse("profiles_delete_object", kwargs={"pk": self.pk})

    # photo
    def upload_full_photo_url(self):
        return reverse("profiles_upload_full_photo", kwargs={"pk": self.pk})

    def get_photo_modal_url(self):
        return reverse("profiles_get_photo_modal", kwargs={"pk": self.pk})

    def remove_photo_modal_url(self):
        return reverse("profiles_remove_photo_modal", kwargs={"pk": self.pk})

    def delete_photos_url(self):
        return reverse("profiles_delete_photos", kwargs={"pk": self.pk})

    def crop_photo_url(self):
        return reverse("profiles_crop_photo", kwargs={"pk": self.pk})

    # personal information
    def save_personal_information_url(self):
        return reverse("profiles_save_personal_information", kwargs={"pk": self.pk})

    # description_slug
    def update_description_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION_LABEL},
        )

    # skill_slug
    def update_skill_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL_LABEL},
        )

    # language_slug
    def update_language_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE_LABEL},
        )

    # education_slug
    def update_education_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION_LABEL},
        )

    # experience_slug
    def update_experience_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE_LABEL},
        )

    # certification_slug
    def update_certification_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION_LABEL},
        )

    # course_slug
    def update_course_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE_LABEL},
        )

    # honor_slug
    def update_honor_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR_LABEL},
        )

    # organization_slug
    def update_organization_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION_LABEL},
        )

    # patent_slug
    def update_patent_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT_LABEL},
        )

    # project_slug
    def update_project_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT_LABEL},
        )

    # publication_slug
    def update_publication_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION_LABEL},
        )

    # volunteering_slug
    def update_volunteering_slug_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING_LABEL},
        )

    # firstname
    def update_firstname_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FIRSTNAME},
        )

    # lastname
    def update_lastname_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LASTNAME},
        )

    # jobtitle
    def update_jobtitle_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_JOBTITLE},
        )

    def activate_jobtitle_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_JOBTITLE},
        )

    def deactivate_jobtitle_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_JOBTITLE},
        )

    def insert_jobtitle_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_JOBTITLE},
        )

    def remove_jobtitle_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_JOBTITLE},
        )

    def insert_jobtitle_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_JOBTITLE},
        )

    def remove_jobtitle_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_JOBTITLE},
        )

    # location
    def update_location_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LOCATION},
        )

    def activate_location_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LOCATION},
        )

    def deactivate_location_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LOCATION},
        )

    def insert_location_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LOCATION},
        )

    def remove_location_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LOCATION},
        )

    def insert_location_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LOCATION},
        )

    def remove_location_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LOCATION},
        )

    # birth
    def update_birth_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_BIRTH},
        )

    def activate_birth_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_BIRTH},
        )

    def deactivate_birth_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_BIRTH},
        )

    def insert_birth_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_BIRTH},
        )

    def remove_birth_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_BIRTH},
        )

    def insert_birth_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_BIRTH},
        )

    def remove_birth_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_BIRTH},
        )

    # phone
    def update_phone_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_PHONE},
        )

    def activate_phone_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_PHONE},
        )

    def deactivate_phone_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_PHONE},
        )

    def insert_phone_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_PHONE},
        )

    def remove_phone_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_PHONE},
        )

    def insert_phone_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_PHONE},
        )

    def remove_phone_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_PHONE},
        )

    # email
    def update_email_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_EMAIL},
        )

    def activate_email_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_EMAIL},
        )

    def deactivate_email_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_EMAIL},
        )

    def insert_email_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_EMAIL},
        )

    def remove_email_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_EMAIL},
        )

    def insert_email_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_EMAIL},
        )

    def remove_email_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_EMAIL},
        )

    # website
    def update_website_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_WEBSITE},
        )

    def activate_website_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_WEBSITE},
        )

    def deactivate_website_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_WEBSITE},
        )

    def insert_website_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_WEBSITE},
        )

    def remove_website_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_WEBSITE},
        )

    def insert_website_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_WEBSITE},
        )

    def remove_website_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_WEBSITE},
        )

    # linkedin
    def update_linkedin_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LINKEDIN},
        )

    def activate_linkedin_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LINKEDIN},
        )

    def deactivate_linkedin_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LINKEDIN},
        )

    def insert_linkedin_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LINKEDIN},
        )

    def remove_linkedin_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LINKEDIN},
        )

    def insert_linkedin_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LINKEDIN},
        )

    def remove_linkedin_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_LINKEDIN},
        )

    # skype
    def update_skype_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_SKYPE},
        )

    def activate_skype_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_SKYPE},
        )

    def deactivate_skype_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_SKYPE},
        )

    def insert_skype_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_SKYPE},
        )

    def remove_skype_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_SKYPE},
        )

    def insert_skype_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_SKYPE},
        )

    def remove_skype_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_SKYPE},
        )

    # instagram
    def update_instagram_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_INSTAGRAM},
        )

    def activate_instagram_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_INSTAGRAM},
        )

    def deactivate_instagram_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_INSTAGRAM},
        )

    def insert_instagram_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_INSTAGRAM},
        )

    def remove_instagram_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_INSTAGRAM},
        )

    def insert_instagram_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_INSTAGRAM},
        )

    def remove_instagram_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_INSTAGRAM},
        )

    # twitter
    def update_twitter_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_TWITTER},
        )

    def activate_twitter_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_TWITTER},
        )

    def deactivate_twitter_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_TWITTER},
        )

    def insert_twitter_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_TWITTER},
        )

    def remove_twitter_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_TWITTER},
        )

    def insert_twitter_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_TWITTER},
        )

    def remove_twitter_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_TWITTER},
        )

    # facebook
    def update_facebook_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FACEBOOK},
        )

    def activate_facebook_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FACEBOOK},
        )

    def deactivate_facebook_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FACEBOOK},
        )

    def insert_facebook_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FACEBOOK},
        )

    def remove_facebook_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FACEBOOK},
        )

    def insert_facebook_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FACEBOOK},
        )

    def remove_facebook_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_FACEBOOK},
        )

    # youtube
    def update_youtube_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_YOUTUBE},
        )

    def activate_youtube_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_YOUTUBE},
        )

    def deactivate_youtube_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_YOUTUBE},
        )

    def insert_youtube_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_YOUTUBE},
        )

    def remove_youtube_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_YOUTUBE},
        )

    def insert_youtube_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_YOUTUBE},
        )

    def remove_youtube_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_YOUTUBE},
        )

    # github
    def update_github_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITHUB},
        )

    def activate_github_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITHUB},
        )

    def deactivate_github_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITHUB},
        )

    def insert_github_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITHUB},
        )

    def remove_github_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITHUB},
        )

    def insert_github_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITHUB},
        )

    def remove_github_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITHUB},
        )

    # gitlab
    def update_gitlab_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITLAB},
        )

    def activate_gitlab_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITLAB},
        )

    def deactivate_gitlab_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITLAB},
        )

    def insert_gitlab_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITLAB},
        )

    def remove_gitlab_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITLAB},
        )

    def insert_gitlab_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITLAB},
        )

    def remove_gitlab_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_GITLAB},
        )

    # stackoverflow
    def update_stackoverflow_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW},
        )

    def activate_stackoverflow_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW,
            },
        )

    def deactivate_stackoverflow_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW,
            },
        )

    def insert_stackoverflow_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW,
            },
        )

    def remove_stackoverflow_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW,
            },
        )

    def insert_stackoverflow_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW,
            },
        )

    def remove_stackoverflow_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW,
            },
        )

    # medium
    def update_medium_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_MEDIUM},
        )

    def activate_medium_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_MEDIUM},
        )

    def deactivate_medium_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_MEDIUM},
        )

    def insert_medium_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_MEDIUM},
        )

    def remove_medium_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_MEDIUM},
        )

    def insert_medium_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_MEDIUM},
        )

    def remove_medium_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_MEDIUM},
        )

    # orcid
    def update_orcid_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_ORCID},
        )

    def activate_orcid_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_ORCID},
        )

    def deactivate_orcid_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_ORCID},
        )

    def insert_orcid_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_ORCID},
        )

    def remove_orcid_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_ORCID},
        )

    def insert_orcid_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_ORCID},
        )

    def remove_orcid_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_ORCID},
        )

    # description
    def update_description_url(self):
        return reverse(
            "profiles_update_field",
            kwargs={"pk": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION},
        )

    def activate_description_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION},
        )

    def deactivate_description_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION},
        )

    def insert_description_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION},
        )

    def remove_description_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION},
        )

    def insert_description_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION},
        )

    def remove_description_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_PROFILE_FIELD_DESCRIPTION},
        )

    # skill
    def create_skill_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def insert_skill_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def remove_skill_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def activate_skill_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def deactivate_skill_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def insert_skill_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def remove_skill_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def insert_skill_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    def remove_skill_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_SKILL},
        )

    # language
    def create_language_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def insert_language_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def remove_language_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def activate_language_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def deactivate_language_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def insert_language_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def remove_language_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def insert_language_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    def remove_language_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE},
        )

    # education
    def create_education_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def insert_education_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def remove_education_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def activate_education_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def deactivate_education_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def insert_education_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def remove_education_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def insert_education_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    def remove_education_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION},
        )

    # experience
    def create_experience_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def insert_experience_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def remove_experience_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def activate_experience_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def deactivate_experience_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def insert_experience_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def remove_experience_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def insert_experience_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    def remove_experience_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE},
        )

    # certification
    def create_certification_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def insert_certification_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def remove_certification_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def activate_certification_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def deactivate_certification_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def insert_certification_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def remove_certification_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def insert_certification_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def remove_certification_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={
                "pk_parent": self.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    # course
    def create_course_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def insert_course_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def remove_course_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def activate_course_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def deactivate_course_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def insert_course_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def remove_course_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def insert_course_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    def remove_course_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_COURSE},
        )

    # honor
    def create_honor_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def insert_honor_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def remove_honor_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def activate_honor_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def deactivate_honor_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def insert_honor_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def remove_honor_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def insert_honor_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    def remove_honor_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_HONOR},
        )

    # organization
    def create_organization_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def insert_organization_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def remove_organization_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def activate_organization_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def deactivate_organization_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def insert_organization_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def remove_organization_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def insert_organization_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    def remove_organization_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION},
        )

    # patent
    def create_patent_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def insert_patent_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def remove_patent_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def activate_patent_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def deactivate_patent_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def insert_patent_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def remove_patent_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def insert_patent_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    def remove_patent_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PATENT},
        )

    # project
    def create_project_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def insert_project_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def remove_project_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def activate_project_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def deactivate_project_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def insert_project_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def remove_project_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def insert_project_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    def remove_project_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PROJECT},
        )

    # publication
    def create_publication_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def insert_publication_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def remove_publication_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def activate_publication_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def deactivate_publication_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def insert_publication_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def remove_publication_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def insert_publication_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    def remove_publication_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION},
        )

    # volunteering
    def create_volunteering_object_url(self):
        return reverse(
            "profiles_create_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def insert_volunteering_new_form_url(self):
        return reverse(
            "profiles_insert_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def remove_volunteering_new_form_url(self):
        return reverse(
            "profiles_remove_child_new_form",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def activate_volunteering_url(self):
        return reverse(
            "profiles_activate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def deactivate_volunteering_url(self):
        return reverse(
            "profiles_deactivate_child_object",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def insert_volunteering_activation_button_url(self):
        return reverse(
            "profiles_insert_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def remove_volunteering_activation_button_url(self):
        return reverse(
            "profiles_remove_child_activation_button",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def insert_volunteering_help_modal_url(self):
        return reverse(
            "profiles_insert_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    def remove_volunteering_help_modal_url(self):
        return reverse(
            "profiles_remove_child_or_field_help_modal",
            kwargs={"pk_parent": self.pk, "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING},
        )

    # resume templates modal
    def remove_resume_templates_modal_url(self):
        return reverse("profiles_remove_resume_templates_modal", kwargs={"pk": self.pk})

    def insert_resume_templates_modal_url(self):
        return reverse("profiles_insert_resume_templates_modal", kwargs={"pk": self.pk})

    #  get list of resumes
    def get_resume_file_list_url(self):
        return reverse("profiles_resume_file_list", kwargs={"pk": self.pk})

    #  insert button to generate resumes
    def insert_button_to_generate_resumes_url(self):
        return reverse(
            "profiles_insert_button_to_generate_resumes", kwargs={"pk": self.pk}
        )

    #  start creating resumes url
    def generate_resumes_url(self):
        return reverse("profiles_generate_resumes", kwargs={"pk": self.pk})

    #  get status
    def resume_creation_status_url(self):
        return reverse(
            "profiles_resume_creation_status",
            kwargs={"pk": self.pk, "task_id": self.task_id},
        )

    # for testing / development
    def generate_resume_testing_url(self):
        return reverse("profiles_generate_resume_testing", kwargs={"pk": self.pk})

    # number of children created // start creating files
    def number_of_children_created(self):
        count_array = [
            self.skill_set.count(),
            self.language_set.count(),
            self.education_set.count(),
            self.experience_set.count(),
            self.certification_set.count(),
            self.course_set.count(),
            self.honor_set.count(),
            self.organization_set.count(),
            self.patent_set.count(),
            self.project_set.count(),
            self.publication_set.count(),
            self.volunteering_set.count(),
        ]
        return sum(count_array)

    # update any field
    def update_field(self, slug, request):
        try:
            new_value = request.POST.get(PROFILE_FIELD_MAPPING[slug])
            setattr(self, slug, new_value)
            self.save()
        except KeyError:
            pass

    def crop_and_save_photo(self, x, y, width, height):
        if self.photo_full:
            photo_full_copy = ContentFile(self.photo_full.read())
            photo_initial = self.photo_full.name.split("/")[-1]
            self.photo.save(photo_initial, photo_full_copy)
            image = Image.open(self.photo)
            cropping_area = (x, y, x + width, y + height)
            cropped_image = image.crop(cropping_area)
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(self.photo.path)
            return self

        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo_full != None:
            try:
                img = Image.open(self.photo_full)
                if img.height > 1200 or img.width > 1200:
                    new_size = (
                        1200,
                        1200,
                    )  # image proportion is manteined / we dont need to do extra work
                    img.thumbnail(new_size)
                    img.save(self.photo_full.path)
            except:
                pass


# class Photo(auto_prefetch.Model):
#     pass


# class FirstName(auto_prefetch.Model):
#     profile = models.OneToOneField(Profile, verbose_name=_(""), on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     active = models.BooleanField(default=True)


class Skill(auto_prefetch.Model):
    """
    An object representing the skills that the member holds.
    See Skill Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/skill
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="skill_set"
    )
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=50)  # Linkedin does not include this

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("-level",)

    def __str__(self):
        return self.name

    @property
    def level_base_5_int(self):
        return (self.level * 5 / 100).__round__()

    @property
    def level_base_6_float(self):
        return self.level * 6 / 100

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_SKILL,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_SKILL,
            },
        )


class Language(auto_prefetch.Model):
    """
    An object representing the languages that the member holds.
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="language_set"
    )
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=3)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "id",
            "level",
        )

    def __str__(self):
        return self.name

    @property
    def level_base_5_int(self):
        return (self.level * 5 / 100).__round__()

    @property
    def level_base_6_float(self):
        return self.level * 6 / 100

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_LANGUAGE,
            },
        )


class Education(auto_prefetch.Model):
    """
    An object representing the member's educational background.
    See Education Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/education
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="education_set"
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    grade = models.CharField(null=True, blank=True, max_length=20)
    institution = models.CharField(null=True, blank=True, max_length=100)
    institution_link = models.CharField(null=True, blank=True, max_length=200)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True, max_length=300)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def __str__(self):
        return self.title

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EDUCATION,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Experience(auto_prefetch.Model):
    """
    Employment history. See Positions for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="experience_set"
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    location = models.CharField(null=True, blank=True, max_length=100)
    company = models.CharField(null=True, blank=True, max_length=100)
    company_link = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def __str__(self):
        return self.title

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_EXPERIENCE,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Certification(auto_prefetch.Model):
    """
    An object representing the certifications that the member holds.
    See Certification Fields for a description of the fields available within this object.
    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/certification
    """

    profile = auto_prefetch.ForeignKey(
        Profile, related_name="certification_set", on_delete=models.CASCADE
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_CERTIFICATION,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Course(auto_prefetch.Model):
    """
    An object representing courses the member has taken.
    See Course Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/course
    """

    profile = auto_prefetch.ForeignKey(
        Profile, related_name="course_set", on_delete=models.CASCADE
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    hours = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_COURSE,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Honor(auto_prefetch.Model):
    """
    An object representing the various honors and awards the member has received.
    See Honor Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/honor
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="honor_set"
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)
    # description = models.TextField(null=True, blank=True)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_HONOR,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Organization(auto_prefetch.Model):
    """
    An object representing the organizations that the member is in.
    See Organization Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/organization
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="organization_set"
    )
    order = models.SmallIntegerField(default=0)

    role = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    organization_link = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_ORGANIZATION,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Patent(auto_prefetch.Model):
    """
    An object representing the various patents associated with the member.
    See Patent Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/patent
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="patent_set"
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=15)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(
        null=True, blank=True, max_length=100
    )  # when pending = False
    inventors = models.CharField(null=True, blank=True, max_length=200)
    link = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(
        null=True, blank=True
    )  # suggest to use to include if the patent is patent is pending and more relevant info

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PATENT,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Project(auto_prefetch.Model):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="project_set"
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    role = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PROJECT,
            },
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Publication(auto_prefetch.Model):
    """
    An object representing the various publications associated with the member.
    See Publication Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="publication_set"
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=200)
    issuing_date = models.CharField(null=True, blank=True, max_length=20)
    authors = models.CharField(null=True, blank=True, max_length=200)
    publisher = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_PUBLICATION,
            },
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Volunteering(auto_prefetch.Model):
    """
    An object representing the member's volunteering experience.
    See Volunteering Experience Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/volunteering-experience
    """

    profile = auto_prefetch.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="volunteering_set"
    )
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    location = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    organization_link = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta(auto_prefetch.Model.Meta):
        ordering = (
            "order",
            "id",
        )

    def update_object_url(self):
        return reverse(
            "profiles_update_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
            },
        )

    def delete_object_url(self):
        return reverse(
            "profiles_delete_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
            },
        )

    def move_up_object_url(self):
        return reverse(
            "profiles_move_up_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
            },
        )

    def move_down_object_url(self):
        return reverse(
            "profiles_move_down_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
            },
        )

    def copy_object_url(self):
        return reverse(
            "profiles_copy_child_object",
            kwargs={
                "pk": self.pk,
                "pk_parent": self.profile.pk,
                "slug": SLUG_FOR_CHILD_OBJECT_VOLUNTEERING,
            },
        )

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


def get_child_class(slug):
    if slug == SLUG_FOR_CHILD_OBJECT_SKILL:
        return Skill

    if slug == SLUG_FOR_CHILD_OBJECT_LANGUAGE:
        return Language

    if slug == SLUG_FOR_CHILD_OBJECT_EDUCATION:
        return Education

    if slug == SLUG_FOR_CHILD_OBJECT_EXPERIENCE:
        return Experience

    if slug == SLUG_FOR_CHILD_OBJECT_CERTIFICATION:
        return Certification

    if slug == SLUG_FOR_CHILD_OBJECT_COURSE:
        return Course

    if slug == SLUG_FOR_CHILD_OBJECT_HONOR:
        return Honor

    if slug == SLUG_FOR_CHILD_OBJECT_ORGANIZATION:
        return Organization

    if slug == SLUG_FOR_CHILD_OBJECT_PATENT:
        return Patent

    if slug == SLUG_FOR_CHILD_OBJECT_PROJECT:
        return Project

    if slug == SLUG_FOR_CHILD_OBJECT_PUBLICATION:
        return Publication

    if slug == SLUG_FOR_CHILD_OBJECT_VOLUNTEERING:
        return Volunteering


def update_child_object(slug=None, child_object=None, request=None):
    if slug == SLUG_FOR_CHILD_OBJECT_SKILL:
        child_object.name = request.POST.get("name")
        child_object.level = request.POST.get("level")

    if slug == SLUG_FOR_CHILD_OBJECT_LANGUAGE:
        child_object.name = request.POST.get("name")
        child_object.level = request.POST.get("level")

    if slug == SLUG_FOR_CHILD_OBJECT_EDUCATION:  # education
        child_object.title = request.POST.get("title")
        child_object.grade = request.POST.get("grade")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.institution = request.POST.get("institution")
        child_object.institution_link = request.POST.get("institution_link")
        child_object.description = request.POST.get("description")

    if slug == SLUG_FOR_CHILD_OBJECT_EXPERIENCE:
        child_object.title = request.POST.get("title")
        child_object.location = request.POST.get("location")
        child_object.company = request.POST.get("company")
        child_object.company_link = request.POST.get("company_link")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.description = request.POST.get("description")

    if slug == SLUG_FOR_CHILD_OBJECT_CERTIFICATION:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.issuer = request.POST.get("issuer")
        child_object.link = request.POST.get("link")

    if slug == SLUG_FOR_CHILD_OBJECT_COURSE:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.issuer = request.POST.get("issuer")
        child_object.hours = request.POST.get("hours")
        child_object.link = request.POST.get("link")

    if slug == SLUG_FOR_CHILD_OBJECT_HONOR:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.issuer = request.POST.get("issuer")
        child_object.link = request.POST.get("link")

    if slug == SLUG_FOR_CHILD_OBJECT_ORGANIZATION:
        child_object.role = request.POST.get("role")
        child_object.organization = request.POST.get("organization")
        child_object.organization_link = request.POST.get("organization_link")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.description = request.POST.get("description")

    if slug == SLUG_FOR_CHILD_OBJECT_PATENT:
        child_object.title = request.POST.get("title")
        child_object.number = request.POST.get("number")
        child_object.issuer = request.POST.get("issuer")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.inventors = request.POST.get("inventors")
        child_object.link = request.POST.get("link")
        child_object.description = request.POST.get("description")

    if slug == SLUG_FOR_CHILD_OBJECT_PROJECT:
        child_object.title = request.POST.get("title")
        child_object.role = request.POST.get("role")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.organization = request.POST.get("organization")
        child_object.link = request.POST.get("link")
        child_object.description = request.POST.get("description")

    if slug == SLUG_FOR_CHILD_OBJECT_PUBLICATION:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.authors = request.POST.get("authors")
        child_object.publisher = request.POST.get("publisher")
        child_object.link = request.POST.get("link")
        child_object.description = request.POST.get("description")

    if slug == SLUG_FOR_CHILD_OBJECT_VOLUNTEERING:
        child_object.title = request.POST.get("title")
        child_object.location = request.POST.get("location")
        child_object.organization = request.POST.get("organization")
        child_object.organization_link = request.POST.get("organization_link")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.description = request.POST.get("description")

    child_object.save()


def set_activation_state(slug=None, object=None, active=True):
    if slug == SLUG_FOR_PROFILE_FIELD_FIRSTNAME:
        object.firstname_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_LASTNAME:
        object.lastname_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_JOBTITLE:
        object.jobtitle_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_LOCATION:
        object.location_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_BIRTH:
        object.birth_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_PHONE:
        object.phone_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_EMAIL:
        object.email_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_DESCRIPTION:
        object.description_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_WEBSITE:
        object.website_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_LINKEDIN:
        object.linkedin_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_SKYPE:
        object.skype_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_INSTAGRAM:
        object.instagram_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_TWITTER:
        object.twitter_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_FACEBOOK:
        object.facebook_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_YOUTUBE:
        object.youtube_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_GITHUB:
        object.github_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_GITLAB:
        object.gitlab_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_STACKOVERFLOW:
        object.stackoverflow_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_MEDIUM:
        object.medium_active = active

    if slug == SLUG_FOR_PROFILE_FIELD_ORCID:
        object.orcid_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_SKILL:
        object.skill_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_LANGUAGE:
        object.language_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_EDUCATION:
        object.education_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_EXPERIENCE:
        object.experience_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_CERTIFICATION:
        object.certification_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_COURSE:
        object.course_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_HONOR:
        object.honor_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_ORGANIZATION:
        object.organization_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_PATENT:
        object.patent_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_PROJECT:
        object.project_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_PUBLICATION:
        object.publication_active = active

    if slug == SLUG_FOR_CHILD_OBJECT_VOLUNTEERING:
        object.volunteering_active = active

    object.save()


def get_child_object(slug=None, pk=None, profile=None):
    """
    This function gets an instance object
    """
    Klass = get_child_class(slug)
    return get_object_or_404(Klass, profile=profile, pk=pk)


def create_empty_child_object(slug=None, profile=None):
    """
    This function creates an empty object associated with a profile instance
    """
    Klass = get_child_class(slug)
    return Klass(profile=profile)


def get_above_child_object(slug=None, child_object=None, profile=None):
    """
    This function gets an instance object that is located before the "child_object"
    """
    Klass = get_child_class(slug)
    return Klass.objects.filter(order__lt=child_object.order, profile=profile).last()


def get_below_child_object(slug=None, child_object=None, profile=None):
    """
    This function gets an instance object that is located after the "child_object"
    """
    Klass = get_child_class(slug)
    return Klass.objects.filter(order__gt=child_object.order, profile=profile).first()


####################################################################################

from tex.models import ResumeTemplate


class Resume(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey(
        Profile, null=True, related_name="resume_set", on_delete=models.SET_NULL
    )
    template = auto_prefetch.ForeignKey(
        ResumeTemplate, null=True, on_delete=models.SET_NULL
    )
    image = models.ImageField(null=True, upload_to="resumes/images")
    pdf = models.FileField(null=True, upload_to="resumes/pdfs")

    def download_resume_pdf_url(self):
        return reverse(
            "profiles_get_resume_pdf",
            kwargs={"pk": self.pk, "pk_parent": self.profile.pk},
        )

    def download_resume_image_url(self):
        return reverse(
            "profiles_get_resume_image",
            kwargs={"pk": self.pk, "pk_parent": self.profile.pk},
        )
