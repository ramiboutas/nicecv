import os
import uuid
from io import BytesIO
from PIL import Image

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.core.files import File
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse, reverse_lazy
User = get_user_model()

# Labels. Used in urls (label) & in templates  (profiles/partials/label/file.html)
LABEL_FOR_PROFILE_FIELD_FIRSTNAME = 'firstname'
LABEL_FOR_PROFILE_FIELD_LASTNAME = 'lastname'
LABEL_FOR_PROFILE_FIELD_JOBTITLE = 'jobtitle'
LABEL_FOR_PROFILE_FIELD_LOCATION = 'location'
LABEL_FOR_PROFILE_FIELD_BIRTH = 'birth'
LABEL_FOR_PROFILE_FIELD_PHONE = 'phone'
LABEL_FOR_PROFILE_FIELD_EMAIL = 'email'
LABEL_FOR_PROFILE_FIELD_DESCRIPTION = 'description'
LABEL_FOR_PROFILE_FIELD_WEBSITE = 'website'
LABEL_FOR_PROFILE_FIELD_LINKEDIN = 'linkedin'
LABEL_FOR_PROFILE_FIELD_SKYPE = 'skype'
LABEL_FOR_PROFILE_FIELD_INSTAGRAM = 'instagram'
LABEL_FOR_PROFILE_FIELD_TWITTER = 'twitter'
LABEL_FOR_PROFILE_FIELD_FACEBOOK = 'facebook'
LABEL_FOR_PROFILE_FIELD_YOUTUBE = 'youtube'
LABEL_FOR_PROFILE_FIELD_GITHUB = 'github'
LABEL_FOR_PROFILE_FIELD_GITLAB = 'gitlab'
LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW = 'stackoverflow'
LABEL_FOR_PROFILE_FIELD_MEDIUM = 'medium'

LABEL_FOR_CHILD_OBJECT_SKILL = 'skill'
LABEL_FOR_CHILD_OBJECT_LANGUAGE = 'language'
LABEL_FOR_CHILD_OBJECT_EDUCATION = 'education'
LABEL_FOR_CHILD_OBJECT_EXPERIENCE = 'experience'
LABEL_FOR_CHILD_OBJECT_CERTIFICATION = 'certification'
LABEL_FOR_CHILD_OBJECT_COURSE = 'course'
LABEL_FOR_CHILD_OBJECT_HONOR = 'honor'
LABEL_FOR_CHILD_OBJECT_ORGANIZATION = 'organization'
LABEL_FOR_CHILD_OBJECT_PATENT = 'patent'
LABEL_FOR_CHILD_OBJECT_PROJECT = 'project'
LABEL_FOR_CHILD_OBJECT_PUBLICATION = 'publication'
LABEL_FOR_CHILD_OBJECT_VOLUNTEERING = 'volunteering'

LABEL_FOR_PROFILE_FIELD_DESCRIPTION_LABEL = 'description-label'
LABEL_FOR_CHILD_OBJECT_SKILL_LABEL = 'skill-label'
LABEL_FOR_CHILD_OBJECT_LANGUAGE_LABEL = 'language-label'
LABEL_FOR_CHILD_OBJECT_EDUCATION_LABEL = 'education-label'
LABEL_FOR_CHILD_OBJECT_EXPERIENCE_LABEL = 'experience-label'
LABEL_FOR_CHILD_OBJECT_CERTIFICATION_LABEL = 'certification-label'
LABEL_FOR_CHILD_OBJECT_COURSE_LABEL = 'course-label'
LABEL_FOR_CHILD_OBJECT_HONOR_LABEL = 'honor-label'
LABEL_FOR_CHILD_OBJECT_ORGANIZATION_LABEL = 'organization-label'
LABEL_FOR_CHILD_OBJECT_PATENT_LABEL = 'patent-label'
LABEL_FOR_CHILD_OBJECT_PROJECT_LABEL = 'project-label'
LABEL_FOR_CHILD_OBJECT_PUBLICATION_LABEL = 'publication-label'
LABEL_FOR_CHILD_OBJECT_VOLUNTEERING_LABEL = 'volunteering-label'



def user_directory_path(instance, filename): # not used // 22.01.2022
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    """
    This function saves the user uploads to a specific folder in media
    """
    return '{0}/{1}'.format(instance.username.id, filename)


def manage_instance_ordering(self):
    """
    This function manages the ordering of an instance when it is created
    new_instance.order > max_order_of_objects + 1
    """
    if self._state.adding:
        try:
            current_maximum_order = self.__class__.objects.latest('order').order
            self.order = current_maximum_order + 1
        except:
            pass # exception if objects do not exist


class Profile(models.Model):
    """
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_set')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    task_id = models.CharField(null=True, blank=True, max_length=50)

    # media
    photo = models.ImageField(null=True, blank=True, upload_to='profiles/cropped_photos/')
    photo_full = models.ImageField(null=True, blank=True, upload_to='profiles/full_photos/')

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
    description_label = models.CharField(max_length=100, default=_('About me'))
    skill_label = models.CharField(max_length=100, default=_('Skills'))
    language_label = models.CharField(max_length=100, default=_('Languages'))
    education_label = models.CharField(max_length=100, default=_('Education'))
    experience_label = models.CharField(max_length=100, default=_('Work experience'))
    certification_label = models.CharField(max_length=100, default=_('Certifications'))
    course_label = models.CharField(max_length=100, default=_('Courses'))
    honor_label = models.CharField(max_length=100, default=_('Honors and Awards'))
    organization_label = models.CharField(max_length=100, default=_('Organizations'))
    patent_label = models.CharField(max_length=100, default=_('Patents'))
    project_label = models.CharField(max_length=100, default=_('Projects'))
    publication_label = models.CharField(max_length=100, default=_('Publications'))
    volunteering_label = models.CharField(max_length=100, default=_('Volunteering work'))

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.email}'

    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'

    # profile object
    def get_update_url(self):
        return reverse('profiles_update', kwargs={'pk':self.pk})

    def delete_object_url(self):
        return reverse('profiles_delete_object', kwargs={'pk':self.pk})

    # photo
    def upload_full_photo_url(self):
        return reverse('profiles_upload_full_photo', kwargs={'pk':self.pk})

    def get_photo_modal_url(self):
        return reverse('profiles_get_photo_modal', kwargs={'pk':self.pk})

    def remove_photo_modal_url(self):
        return reverse('profiles_remove_photo_modal', kwargs={'pk':self.pk})

    def delete_photos_url(self):
        return reverse('profiles_delete_photos', kwargs={'pk':self.pk})

    def crop_photo_url(self):
        return reverse('profiles_crop_photo', kwargs={'pk':self.pk})

    # personal information
    def save_personal_information_url(self):
        return reverse('profiles_save_personal_information', kwargs={'pk':self.pk})

    # description_label
    def update_description_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION_LABEL})

    # skill_label
    def update_skill_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL_LABEL})

    # language_label
    def update_language_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE_LABEL})

    # education_label
    def update_education_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION_LABEL})

    # experience_label
    def update_experience_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE_LABEL})

    # certification_label
    def update_certification_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION_LABEL})

    # course_label
    def update_course_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE_LABEL})

    # honor_label
    def update_honor_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR_LABEL})

    # organization_label
    def update_organization_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION_LABEL})

    # patent_label
    def update_patent_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT_LABEL})

    # project_label
    def update_project_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT_LABEL})

    # publication_label
    def update_publication_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION_LABEL})

    # volunteering_label
    def update_volunteering_label_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING_LABEL})

    # firstname
    def update_firstname_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FIRSTNAME})

    # lastname
    def update_lastname_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LASTNAME})

    # jobtitle
    def update_jobtitle_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_JOBTITLE})

    def activate_jobtitle_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_JOBTITLE})

    def deactivate_jobtitle_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_JOBTITLE})

    def insert_jobtitle_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_JOBTITLE})

    def remove_jobtitle_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_JOBTITLE})

    def insert_jobtitle_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_JOBTITLE})

    def remove_jobtitle_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_JOBTITLE})

    # location
    def update_location_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LOCATION})

    def activate_location_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LOCATION})

    def deactivate_location_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LOCATION})

    def insert_location_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LOCATION})

    def remove_location_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LOCATION})

    def insert_location_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LOCATION})

    def remove_location_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LOCATION})

    # birth
    def update_birth_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_BIRTH})

    def activate_birth_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_BIRTH})

    def deactivate_birth_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_BIRTH})

    def insert_birth_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_BIRTH})

    def remove_birth_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_BIRTH})

    def insert_birth_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_BIRTH})

    def remove_birth_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_BIRTH})

    # phone
    def update_phone_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_PHONE})

    def activate_phone_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_PHONE})

    def deactivate_phone_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_PHONE})

    def insert_phone_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_PHONE})

    def remove_phone_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_PHONE})

    def insert_phone_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_PHONE})

    def remove_phone_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_PHONE})

    # email
    def update_email_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_EMAIL})

    def activate_email_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_EMAIL})

    def deactivate_email_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_EMAIL})

    def insert_email_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_EMAIL})

    def remove_email_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_EMAIL})

    def insert_email_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_EMAIL})

    def remove_email_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_EMAIL})

    # website
    def update_website_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_WEBSITE})

    def activate_website_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_WEBSITE})

    def deactivate_website_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_WEBSITE})

    def insert_website_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_WEBSITE})

    def remove_website_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_WEBSITE})

    def insert_website_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_WEBSITE})

    def remove_website_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_WEBSITE})

    # linkedin
    def update_linkedin_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LINKEDIN})

    def activate_linkedin_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LINKEDIN})

    def deactivate_linkedin_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LINKEDIN})

    def insert_linkedin_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LINKEDIN})

    def remove_linkedin_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LINKEDIN})

    def insert_linkedin_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LINKEDIN})

    def remove_linkedin_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_LINKEDIN})

    # skype
    def update_skype_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_SKYPE})

    def activate_skype_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_SKYPE})

    def deactivate_skype_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_SKYPE})

    def insert_skype_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_SKYPE})

    def remove_skype_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_SKYPE})

    def insert_skype_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_SKYPE})

    def remove_skype_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_SKYPE})

    # instagram
    def update_instagram_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_INSTAGRAM})

    def activate_instagram_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_INSTAGRAM})

    def deactivate_instagram_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_INSTAGRAM})

    def insert_instagram_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_INSTAGRAM})

    def remove_instagram_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_INSTAGRAM})

    def insert_instagram_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_INSTAGRAM})

    def remove_instagram_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_INSTAGRAM})

    # twitter
    def update_twitter_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_TWITTER})

    def activate_twitter_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_TWITTER})

    def deactivate_twitter_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_TWITTER})

    def insert_twitter_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_TWITTER})

    def remove_twitter_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_TWITTER})

    def insert_twitter_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_TWITTER})

    def remove_twitter_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_TWITTER})


    # facebook
    def update_facebook_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FACEBOOK})

    def activate_facebook_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FACEBOOK})

    def deactivate_facebook_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FACEBOOK})

    def insert_facebook_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FACEBOOK})

    def remove_facebook_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FACEBOOK})

    def insert_facebook_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FACEBOOK})

    def remove_facebook_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_FACEBOOK})

    # youtube
    def update_youtube_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_YOUTUBE})

    def activate_youtube_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_YOUTUBE})

    def deactivate_youtube_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_YOUTUBE})

    def insert_youtube_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_YOUTUBE})

    def remove_youtube_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_YOUTUBE})

    def insert_youtube_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_YOUTUBE})

    def remove_youtube_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_YOUTUBE})

    # github
    def update_github_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITHUB})

    def activate_github_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITHUB})

    def deactivate_github_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITHUB})

    def insert_github_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITHUB})

    def remove_github_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITHUB})

    def insert_github_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITHUB})

    def remove_github_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITHUB})

    # gitlab
    def update_gitlab_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITLAB})

    def activate_gitlab_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITLAB})

    def deactivate_gitlab_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITLAB})

    def insert_gitlab_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITLAB})

    def remove_gitlab_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITLAB})

    def insert_gitlab_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITLAB})

    def remove_gitlab_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_GITLAB})

    # stackoverflow
    def update_stackoverflow_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW})

    def activate_stackoverflow_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW})

    def deactivate_stackoverflow_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW})

    def insert_stackoverflow_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW})

    def remove_stackoverflow_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW})

    def insert_stackoverflow_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW})

    def remove_stackoverflow_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW})

    # medium
    def update_medium_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_MEDIUM})

    def activate_medium_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_MEDIUM})

    def deactivate_medium_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_MEDIUM})

    def insert_medium_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_MEDIUM})

    def remove_medium_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_MEDIUM})

    def insert_medium_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_MEDIUM})

    def remove_medium_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_MEDIUM})

    # description
    def update_description_url(self):
        return reverse('profiles_update_field',
                        kwargs={'pk':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION})

    def activate_description_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION})

    def deactivate_description_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION})

    def insert_description_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION})

    def remove_description_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION})

    def insert_description_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION})

    def remove_description_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_PROFILE_FIELD_DESCRIPTION})

    # skill
    def create_skill_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def insert_skill_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def remove_skill_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def activate_skill_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def deactivate_skill_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def insert_skill_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def remove_skill_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def insert_skill_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def remove_skill_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    # language
    def create_language_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def insert_language_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def remove_language_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def activate_language_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def deactivate_language_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def insert_language_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def remove_language_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def insert_language_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def remove_language_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    # education
    def create_education_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def insert_education_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def remove_education_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def activate_education_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def deactivate_education_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def insert_education_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def remove_education_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})


    def insert_education_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def remove_education_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    # experience
    def create_experience_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def insert_experience_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def remove_experience_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def activate_experience_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def deactivate_experience_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def insert_experience_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def remove_experience_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def insert_experience_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def remove_experience_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    # certification
    def create_certification_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def insert_certification_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def remove_certification_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def activate_certification_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def deactivate_certification_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def insert_certification_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def remove_certification_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def insert_certification_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def remove_certification_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    # course
    def create_course_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def insert_course_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def remove_course_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def activate_course_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def deactivate_course_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def insert_course_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def remove_course_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def insert_course_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def remove_course_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    # honor
    def create_honor_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def insert_honor_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def remove_honor_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def activate_honor_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def deactivate_honor_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def insert_honor_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def remove_honor_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def insert_honor_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def remove_honor_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    # organization
    def create_organization_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def insert_organization_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def remove_organization_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def activate_organization_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def deactivate_organization_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def insert_organization_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def remove_organization_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def insert_organization_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def remove_organization_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    # patent
    def create_patent_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def insert_patent_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def remove_patent_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def activate_patent_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def deactivate_patent_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def insert_patent_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def remove_patent_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def insert_patent_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def remove_patent_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    # project
    def create_project_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def insert_project_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def remove_project_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def activate_project_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def deactivate_project_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def insert_project_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def remove_project_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def insert_project_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def remove_project_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    # publication
    def create_publication_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def insert_publication_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def remove_publication_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def activate_publication_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def deactivate_publication_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def insert_publication_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def remove_publication_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def insert_publication_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def remove_publication_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    # volunteering
    def create_volunteering_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def insert_volunteering_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def remove_volunteering_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def activate_volunteering_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def deactivate_volunteering_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def insert_volunteering_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def remove_volunteering_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def insert_volunteering_help_modal_url(self):
        return reverse('profiles_insert_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def remove_volunteering_help_modal_url(self):
        return reverse('profiles_remove_child_or_field_help_modal',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    # resume templates modal
    def remove_resume_templates_modal_url(self):
        return reverse('profiles_remove_resume_templates_modal', kwargs={'pk':self.pk})

    def insert_resume_templates_modal_url(self):
        return reverse('profiles_insert_resume_templates_modal', kwargs={'pk':self.pk})

    #  get resume file
    def get_resume_file_list_url(self):
        return reverse('files_resume_file_list', kwargs={'pk':self.pk})

    #  start creating resumes url
    def generate_resumes_url(self):
        return reverse('files_generate_resumes', kwargs={'pk':self.pk})

    #  start creating resumes url
    def resume_creation_status_url(self):
        return reverse('files_resume_creation_status', kwargs={'pk':self.pk, 'task_id': self.task_id})



    # number of children created // start creating files
    def number_of_children_created(self):
        count_array = [ self.skill_set.count(),
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
                        self.volunteering_set.count()
                        ]
        return sum(count_array)

    # update any field
    def update_field(self, label, request):

        if label == LABEL_FOR_PROFILE_FIELD_FIRSTNAME:
            self.firstname = request.POST.get("firstname")

        if label == LABEL_FOR_PROFILE_FIELD_LASTNAME:
            self.lastname = request.POST.get("lastname")

        if label == LABEL_FOR_PROFILE_FIELD_JOBTITLE:
            self.jobtitle = request.POST.get("jobtitle")

        if label == LABEL_FOR_PROFILE_FIELD_LOCATION:
            self.location = request.POST.get("location")

        if label == LABEL_FOR_PROFILE_FIELD_BIRTH:
            self.birth = request.POST.get("birth")

        if label == LABEL_FOR_PROFILE_FIELD_PHONE:
            self.phone = request.POST.get("phone")

        if label == LABEL_FOR_PROFILE_FIELD_EMAIL:
            self.email = request.POST.get("email")

        if label == LABEL_FOR_PROFILE_FIELD_DESCRIPTION:
            self.description = request.POST.get("description")

        if label == LABEL_FOR_PROFILE_FIELD_WEBSITE:
            self.website = request.POST.get("website")

        if label == LABEL_FOR_PROFILE_FIELD_SKYPE:
            self.skype = request.POST.get("skype")

        if label == LABEL_FOR_PROFILE_FIELD_INSTAGRAM:
            self.instagram = request.POST.get("instagram")

        if label == LABEL_FOR_PROFILE_FIELD_TWITTER:
            self.linkedin = request.POST.get("linkedin")

        if label == LABEL_FOR_PROFILE_FIELD_FACEBOOK:
            self.linkedin = request.POST.get("linkedin")

        if label == LABEL_FOR_PROFILE_FIELD_YOUTUBE:
            self.linkedin = request.POST.get("linkedin")

        if label == LABEL_FOR_PROFILE_FIELD_GITHUB:
            self.github = request.POST.get("github")

        if label == LABEL_FOR_PROFILE_FIELD_GITLAB:
            self.gitlab = request.POST.get("gitlab")

        if label == LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW:
            self.stackoverflow = request.POST.get("stackoverflow")

        if label == LABEL_FOR_PROFILE_FIELD_MEDIUM:
            self.medium = request.POST.get("medium")

        if label == LABEL_FOR_PROFILE_FIELD_DESCRIPTION_LABEL:
            self.description_label = request.POST.get("description_label")

        if label == LABEL_FOR_CHILD_OBJECT_SKILL_LABEL:
            self.skill_label = request.POST.get("skill_label")

        if label == LABEL_FOR_CHILD_OBJECT_LANGUAGE_LABEL:
            self.language_label = request.POST.get("language_label")

        if label == LABEL_FOR_CHILD_OBJECT_EDUCATION_LABEL:
            self.education_label = request.POST.get("education_label")

        if label == LABEL_FOR_CHILD_OBJECT_EXPERIENCE_LABEL:
            self.experience_label = request.POST.get("experience_label")

        if label == LABEL_FOR_CHILD_OBJECT_CERTIFICATION_LABEL:
            self.certification_label = request.POST.get("certification_label")

        if label == LABEL_FOR_CHILD_OBJECT_COURSE_LABEL:
            self.course_label = request.POST.get("course_label")

        if label == LABEL_FOR_CHILD_OBJECT_HONOR_LABEL:
            self.honor_label = request.POST.get("honor_label")

        if label == LABEL_FOR_CHILD_OBJECT_ORGANIZATION_LABEL:
            self.organization_label = request.POST.get("organization_label")

        if label == LABEL_FOR_CHILD_OBJECT_PATENT_LABEL:
            self.patent_label = request.POST.get("patent_label")

        if label == LABEL_FOR_CHILD_OBJECT_PROJECT_LABEL:
            self.project_label = request.POST.get("project_label")

        if label == LABEL_FOR_CHILD_OBJECT_PUBLICATION_LABEL:
            self.publication_label = request.POST.get("publication_label")

        if label == LABEL_FOR_CHILD_OBJECT_VOLUNTEERING_LABEL:
            self.volunteering_label = request.POST.get("volunteering_label")

        self.save()

    def crop_and_save_photo(self, x, y, width, height):
        if self.photo_full:
            photo_full_copy = ContentFile(self.photo_full.read())
            photo_initial = self.photo_full.name.split("/")[-1]
            self.photo.save(photo_initial, photo_full_copy)
            image = Image.open(self.photo)
            cropping_area = (x, y, x+width, y+height)
            cropped_image = image.crop(cropping_area)
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(self.photo.path)
            return self

        return None

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.photo_full != None:
            try:
                img = Image.open(self.photo_full)
                if img.height > 1200 or img.width > 1200:
                    new_size = (1200, 1200) # image proportion is manteined / we dont need to do extra work
                    img.thumbnail(new_size)
                    img.save(self.photo_full.path)
            except:
                pass


class Skill(models.Model):
    """
    An object representing the skills that the member holds.
    See Skill Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/skill
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skill_set')
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=50) # Linkedin does not include this

    class Meta:
        ordering = ('-level', )

    def __str__(self):
        return self.name

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_SKILL})


class Language(models.Model):
    """
    An object representing the languages that the member holds.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='language_set')
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=50)

    class Meta:
        ordering = ('id', 'level', )

    def __str__(self):
        return self.name

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})


class Education(models.Model):
    """
    An object representing the member's educational background.
    See Education Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/education
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education_set')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    grade = models.CharField(null=True, blank=True, max_length=20)
    institution = models.CharField(null=True, blank=True, max_length=100)
    institution_link = models.CharField(null=True, blank=True, max_length=200)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True, max_length=300)

    class Meta:
        ordering = ('order', 'id', )

    def __str__(self):
        return self.title

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Experience(models.Model):
    """
    Employment history. See Positions for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience_set')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    location = models.CharField(null=True, blank=True, max_length=100)
    company = models.CharField(null=True, blank=True, max_length=100)
    company_link = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta:
        ordering = ('order', 'id', )

    def __str__(self):
        return self.title
    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Certification(models.Model):
    """
    An object representing the certifications that the member holds.
    See Certification Fields for a description of the fields available within this object.
    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/certification
    """
    profile = models.ForeignKey(Profile, related_name='certification_set', on_delete=models.CASCADE)
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Course(models.Model):
    """
    An object representing courses the member has taken.
    See Course Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/course
    """
    profile = models.ForeignKey(Profile, related_name='course_set', on_delete=models.CASCADE)
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    hours = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Honor(models.Model):
    """
    An object representing the various honors and awards the member has received.
    See Honor Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/honor
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='honor_set')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)
    # description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Organization(models.Model):
    """
    An object representing the organizations that the member is in.
    See Organization Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/organization
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organization_set')
    order = models.SmallIntegerField(default=0)

    role = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    organization_link = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Patent(models.Model):
    """
    An object representing the various patents associated with the member.
    See Patent Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/patent
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patent_set')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=15)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    issuing_date = models.CharField(null=True, blank=True, max_length=100) # when pending = False
    inventors = models.CharField(null=True, blank=True, max_length=200)
    link = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True) # suggest to use to include if the patent is patent is pending and more relevant info

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Project(models.Model):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='project_set')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    role = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Publication(models.Model):
    """
    An object representing the various publications associated with the member.
    See Publication Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publication_set')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=200)
    issuing_date = models.CharField(null=True, blank=True, max_length=20)
    authors = models.CharField(null=True, blank=True, max_length=200)
    publisher = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Volunteering(models.Model):
    """
    An object representing the member's volunteering experience.
    See Volunteering Experience Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/volunteering-experience
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='volunteering_set')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    location = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    organization_link = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta:
        ordering = ('order', 'id', )

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


def get_child_class(label):

    if label == LABEL_FOR_CHILD_OBJECT_SKILL:
        return Skill

    if label == LABEL_FOR_CHILD_OBJECT_LANGUAGE:
        return Language

    if label == LABEL_FOR_CHILD_OBJECT_EDUCATION:
        return Education

    if label == LABEL_FOR_CHILD_OBJECT_EXPERIENCE:
        return Experience

    if label == LABEL_FOR_CHILD_OBJECT_CERTIFICATION:
        return Certification

    if label == LABEL_FOR_CHILD_OBJECT_COURSE:
        return Course

    if label == LABEL_FOR_CHILD_OBJECT_HONOR:
        return Honor

    if label == LABEL_FOR_CHILD_OBJECT_ORGANIZATION:
        return Organization

    if label == LABEL_FOR_CHILD_OBJECT_PATENT:
        return Patent

    if label == LABEL_FOR_CHILD_OBJECT_PROJECT:
        return Project

    if label == LABEL_FOR_CHILD_OBJECT_PUBLICATION:
        return Publication

    if label == LABEL_FOR_CHILD_OBJECT_VOLUNTEERING:
        return Volunteering


def update_child_object(label=None, child_object=None, request=None):

    if label == LABEL_FOR_CHILD_OBJECT_SKILL:
        child_object.name = request.POST.get("name")
        child_object.level = request.POST.get("level")

    if label == LABEL_FOR_CHILD_OBJECT_LANGUAGE:
        child_object.name = request.POST.get("name")
        child_object.level = request.POST.get("level")

    if label == LABEL_FOR_CHILD_OBJECT_EDUCATION: # education
        child_object.title = request.POST.get("title")
        child_object.grade = request.POST.get("grade")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.institution = request.POST.get("institution")
        child_object.institution_link = request.POST.get("institution_link")
        child_object.description = request.POST.get("description")

    if label == LABEL_FOR_CHILD_OBJECT_EXPERIENCE:
        child_object.title = request.POST.get("title")
        child_object.location = request.POST.get("location")
        child_object.company = request.POST.get("company")
        child_object.company_link = request.POST.get("company_link")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.description = request.POST.get("description")

    if label == LABEL_FOR_CHILD_OBJECT_CERTIFICATION:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.issuer = request.POST.get("issuer")
        child_object.link = request.POST.get("link")

    if label == LABEL_FOR_CHILD_OBJECT_COURSE:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.issuer = request.POST.get("issuer")
        child_object.hours = request.POST.get("hours")
        child_object.link = request.POST.get("link")

    if label == LABEL_FOR_CHILD_OBJECT_HONOR:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.issuer = request.POST.get("issuer")
        child_object.link = request.POST.get("link")

    if label == LABEL_FOR_CHILD_OBJECT_ORGANIZATION:
        child_object.role = request.POST.get("role")
        child_object.organization = request.POST.get("organization")
        child_object.organization_link = request.POST.get("organization_link")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.description = request.POST.get("description")

    if label == LABEL_FOR_CHILD_OBJECT_PATENT:
        child_object.title = request.POST.get("title")
        child_object.number = request.POST.get("number")
        child_object.issuer = request.POST.get("issuer")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.inventors = request.POST.get("inventors")
        child_object.link = request.POST.get("link")
        child_object.description = request.POST.get("description")

    if label == LABEL_FOR_CHILD_OBJECT_PROJECT:
        child_object.title = request.POST.get("title")
        child_object.role = request.POST.get("role")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.organization = request.POST.get("organization")
        child_object.link = request.POST.get("link")
        child_object.description = request.POST.get("description")

    if label == LABEL_FOR_CHILD_OBJECT_PUBLICATION:
        child_object.title = request.POST.get("title")
        child_object.issuing_date = request.POST.get("issuing_date")
        child_object.authors = request.POST.get("authors")
        child_object.publisher = request.POST.get("publisher")
        child_object.link = request.POST.get("link")
        child_object.description = request.POST.get("description")

    if label == LABEL_FOR_CHILD_OBJECT_VOLUNTEERING:
        child_object.title = request.POST.get("title")
        child_object.location = request.POST.get("location")
        child_object.organization = request.POST.get("organization")
        child_object.organization_link = request.POST.get("organization_link")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.description = request.POST.get("description")

    child_object.save()


def set_activation_state(label=None, object=None, active=True):

    if label == LABEL_FOR_PROFILE_FIELD_FIRSTNAME:
        object.firstname_active = active

    if label == LABEL_FOR_PROFILE_FIELD_LASTNAME:
        object.lastname_active = active

    if label == LABEL_FOR_PROFILE_FIELD_JOBTITLE:
        object.jobtitle_active = active

    if label == LABEL_FOR_PROFILE_FIELD_LOCATION:
        object.location_active = active

    if label == LABEL_FOR_PROFILE_FIELD_BIRTH:
        object.birth_active = active

    if label == LABEL_FOR_PROFILE_FIELD_PHONE:
        object.phone_active = active

    if label == LABEL_FOR_PROFILE_FIELD_EMAIL:
        object.email_active = active

    if label == LABEL_FOR_PROFILE_FIELD_DESCRIPTION:
        object.description_active = active

    if label == LABEL_FOR_PROFILE_FIELD_WEBSITE:
        object.website_active = active

    if label == LABEL_FOR_PROFILE_FIELD_LINKEDIN:
        object.linkedin_active = active

    if label == LABEL_FOR_PROFILE_FIELD_SKYPE:
        object.skype_active = active

    if label == LABEL_FOR_PROFILE_FIELD_INSTAGRAM:
        object.instagram_active = active

    if label == LABEL_FOR_PROFILE_FIELD_TWITTER:
        object.twitter_active = active

    if label == LABEL_FOR_PROFILE_FIELD_FACEBOOK:
        object.facebook_active = active

    if label == LABEL_FOR_PROFILE_FIELD_YOUTUBE:
        object.youtube_active = active

    if label == LABEL_FOR_PROFILE_FIELD_GITHUB:
        object.github_active = active

    if label == LABEL_FOR_PROFILE_FIELD_GITLAB:
        object.gitlab_active = active

    if label == LABEL_FOR_PROFILE_FIELD_STACKOVERFLOW:
        object.stackoverflow_active = active

    if label == LABEL_FOR_PROFILE_FIELD_MEDIUM:
        object.medium_active = active

    if label == LABEL_FOR_CHILD_OBJECT_SKILL:
        object.skill_active = active

    if label == LABEL_FOR_CHILD_OBJECT_LANGUAGE:
        object.language_active = active

    if label == LABEL_FOR_CHILD_OBJECT_EDUCATION:
        object.education_active = active

    if label == LABEL_FOR_CHILD_OBJECT_EXPERIENCE:
        object.experience_active = active

    if label == LABEL_FOR_CHILD_OBJECT_CERTIFICATION:
        object.certification_active = active

    if label == LABEL_FOR_CHILD_OBJECT_COURSE:
        object.course_active = active

    if label == LABEL_FOR_CHILD_OBJECT_HONOR:
        object.honor_active = active

    if label == LABEL_FOR_CHILD_OBJECT_ORGANIZATION:
        object.organization_active = active

    if label == LABEL_FOR_CHILD_OBJECT_PATENT:
        object.patent_active = active

    if label == LABEL_FOR_CHILD_OBJECT_PROJECT:
        object.project_active = active

    if label == LABEL_FOR_CHILD_OBJECT_PUBLICATION:
        object.publication_active = active

    if label == LABEL_FOR_CHILD_OBJECT_VOLUNTEERING:
        object.volunteering_active = active

    object.save()


def get_child_object(label=None, pk=None, profile=None):
    """
    This function gets an instance object
    """
    Klass = get_child_class(label)
    return get_object_or_404(Klass, profile=profile, pk=pk)


def create_empty_child_object(label=None, profile=None):
    """
    This function creates an empty object associated with a profile instance
    """
    Klass = get_child_class(label)
    return Klass(profile=profile)


def get_above_child_object(label=None, child_object=None, profile=None):
    """
    This function gets an instance object that is located before the "child_object"
    """
    Klass = get_child_class(label)
    return Klass.objects.filter(order__lt=child_object.order, profile=profile).last()


def get_below_child_object(label=None, child_object=None, profile=None):
    """
    This function gets an instance object that is located after the "child_object"
    """
    Klass = get_child_class(label)
    return Klass.objects.filter(order__gt=child_object.order, profile=profile).first()



###################################################

class Resume(models.Model):
    profile = models.ForeignKey(Profile, related_name="resumes", on_delete=models.CASCADE)
    # texfile = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=settings.RESUME_IMAGE_DIRECTORY) # , upload_to='files/%Y/%m/%d/'
    pdf = models.FileField(null=True , upload_to=settings.RESUME_PDF_DIRECTORY)
