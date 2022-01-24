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

# used in urls (child_label) & in templates  (profiles/partials/child_label/file.html)
LABEL_FOR_PROFILE_FIELD_DESCRIPTION = 'description'

LABEL_FOR_CHILD_OBJECT_WEBSITE = 'website'
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # media
    photo = models.ImageField(null=True, blank=True, upload_to='profiles/cropped_photos/')
    photo_full = models.ImageField(null=True, blank=True, upload_to='profiles/full_photos/')

    # personal info
    first_name = models.CharField(null=True, blank=True, max_length=50)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    maiden_name = models.CharField(null=True, blank=True, max_length=50)
    location = models.CharField(null=True, blank=True, max_length=50)
    date_of_birth = models.CharField(null=True, blank=True, max_length=50)
    jobtitle = models.CharField(max_length=50)

    # contact info
    phone = models.CharField(null=True, blank=True, max_length=50)
    email = models.CharField(max_length=50)

    # description & interests
    description = models.TextField(null=True, blank=True, max_length=1000)
    interests = models.CharField(null=True, blank=True, max_length=200)

    # activation of Fields
    description_active = models.BooleanField(default=True)
    website_active = models.BooleanField(default=True)
    skill_active = models.BooleanField(default=True)
    language_active = models.BooleanField(default=True)
    education_active = models.BooleanField(default=True)
    experience_active = models.BooleanField(default=True)
    certification_active = models.BooleanField(default=False)
    course_active = models.BooleanField(default=True)
    honor_active = models.BooleanField(default=False)
    organization_active = models.BooleanField(default=False)
    honor_active = models.BooleanField(default=False)
    patent_active = models.BooleanField(default=False)
    project_active = models.BooleanField(default=False)
    publication_active = models.BooleanField(default=False)
    volunteering_active = models.BooleanField(default=False)

    # labels
    skill_label = models.CharField(max_length=100, default=_('Skills'))
    position_label = models.CharField(max_length=100, default=_('Work experience'))
    education_label = models.CharField(max_length=100, default=_('Education'))
    publication_label = models.CharField(max_length=100, default=_('Publications'))
    project_label = models.CharField(max_length=100, default=_('Projects'))


    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def activate_child_or_field(self, child_label=None):
        pass

    def get_update_url(self):
        return reverse('profiles_update', kwargs={'pk':self.pk})

    def delete_object_url(self):
        return reverse('profiles_delete_object', kwargs={'pk':self.pk})

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

    def save_personal_information_url(self):
        return reverse('profiles_save_personal_information', kwargs={'pk':self.pk})

    # description
    def update_description_url(self):
        return reverse('profiles_update_description', kwargs={'pk':self.pk})

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


    # _website_
    def create_website_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    def insert_website_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    def remove_website_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    def activate_website_url(self):
        return reverse('profiles_activate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    def deactivate_website_url(self):
        return reverse('profiles_deactivate_child_object',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    def insert_website_activation_button_url(self):
        return reverse('profiles_insert_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    def remove_website_activation_button_url(self):
        return reverse('profiles_remove_child_activation_button',
                        kwargs={'pk_parent':self.pk, 'label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    # _skill_
    def create_skill_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def insert_skill_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def remove_skill_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_SKILL})

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

    # _language_
    def create_language_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def insert_language_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def remove_language_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

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

    # education
    def create_education_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def insert_education_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def remove_education_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

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

    # experience
    def create_experience_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def insert_experience_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def remove_experience_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

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

    # _certification_
    def create_certification_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def insert_certification_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def remove_certification_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

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

    # _course_
    def create_course_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def insert_course_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def remove_course_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

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

    # _honor_
    def create_honor_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def insert_honor_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def remove_honor_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

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

    # _organization_
    def create_organization_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def insert_organization_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def remove_organization_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

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

    # _patent_
    def create_patent_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def insert_patent_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def remove_patent_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

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

    # _project_
    def create_project_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def insert_project_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def remove_project_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

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

    # _publication_
    def create_publication_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def insert_publication_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def remove_publication_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

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

    # _volunteering_
    def create_volunteering_object_url(self):
        return reverse('profiles_create_child_object',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def insert_volunteering_new_form_url(self):
        return reverse('profiles_insert_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def remove_volunteering_new_form_url(self):
        return reverse('profiles_remove_child_new_form',
                        kwargs={'pk_parent':self.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

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
            except ValueError:
                pass



class Website(models.Model):
    """
    Localized websites the member wants displayed on the profile.
    See Website Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/website
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='websites')
    name = models.CharField(null=True, blank=True, max_length=50)
    bootstrap_icon = models.CharField(null=True, blank=True, default='globe', max_length=25)
    # category = models.CharField(null=True, blank=True, max_length=100, choices=settings.PROFILE_website_CHOICES)
    # label = models.CharField(null=True, blank=True, max_length=100) # if other > label

    def __str__(self):
        return self.name

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_WEBSITE})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_WEBSITE})



class Skill(models.Model):
    """
    An object representing the skills that the member holds.
    See Skill Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/skill
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=50) # Linkedin does not include this

    def __str__(self):
        return self.name

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_SKILL})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_SKILL})


class Language(models.Model):
    """
    An object representing the languages that the member holds.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=50, choices=settings.PROFILE_LANGUAGE_LEVEL_CHOICES)

    def __str__(self):
        return self.name

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_LANGUAGE})



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
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EDUCATION})

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
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    company_name = models.CharField(null=True, blank=True, max_length=100)
    location_name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    class Meta:
        ordering = ('order', 'id', )

    def __str__(self):
        return self.title
    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_EXPERIENCE})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Certification(models.Model):
    """
    An object representing the certifications that the member holds.
    See Certification Fields for a description of the fields available within this object.
    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/certification
    """
    profile = models.ForeignKey(Profile, related_name='certifications', on_delete=models.CASCADE)
    order = models.SmallIntegerField(default=0)

    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    name = models.CharField(null=True, blank=True, max_length=100)
    authority = models.CharField(null=True, blank=True, max_length=100)
    company = models.CharField(null=True, blank=True, max_length=100)
    license = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_CERTIFICATION})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Course(models.Model):
    """
    An object representing courses the member has taken.
    See Course Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/course
    """
    profile = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=100)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_COURSE})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Honor(models.Model):
    """
    An object representing the various honors and awards the member has received.
    See Honor Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/honor
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='honors')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    issue_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_HONOR})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Organization(models.Model):
    """
    An object representing the organizations that the member is in.
    See Organization Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/organization
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organizations')
    order = models.SmallIntegerField(default=0)

    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    position = models.CharField(null=True, blank=True, max_length=100)

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_ORGANIZATION})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Patent(models.Model):
    """
    An object representing the various patents associated with the member.
    See Patent Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/patent
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patents')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    inventors = models.CharField(null=True, blank=True, max_length=200)
    pending = models.BooleanField(null=True, blank=True)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    issue_date = models.CharField(null=True, blank=True, max_length=100) # when pending = False
    application_number = models.IntegerField(null=True, blank=True) # when pending = True
    description = models.TextField(null=True, blank=True)
    filling_date = models.CharField(null=True, blank=True, max_length=100) # when pending = True
    number = models.IntegerField(null=True, blank=True) # when pending = False
    url = models.URLField(null=True, blank=True)

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PATENT})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


class Project(models.Model):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    members = models.CharField(null=True, blank=True, max_length=200)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    ongoing = models.BooleanField(null=True, blank=True) # singleDate
    issuer = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PROJECT})

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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    order = models.SmallIntegerField(default=0)

    name = models.CharField(null=True, blank=True, max_length=200)
    date = models.CharField(null=True, blank=True, max_length=20)
    description = models.TextField(null=True, blank=True, max_length=1000)
    authors = models.CharField(null=True, blank=True, max_length=200)
    publisher = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_PUBLICATION})

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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='volunteering_experiences')
    order = models.SmallIntegerField(default=0)

    title = models.CharField(null=True, blank=True, max_length=100)
    role = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)
    cause = models.CharField(null=True, blank=True, max_length=100)
    ongoing = models.BooleanField(null=True, blank=True) # singleDate

    def update_object_url(self):
        return reverse('profiles_update_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def delete_object_url(self):
        return reverse('profiles_delete_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def move_up_object_url(self):
        return reverse('profiles_move_up_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def move_down_object_url(self):
        return reverse('profiles_move_down_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def copy_object_url(self):
        return reverse('profiles_copy_child_object',
                        kwargs={'pk':self.pk, 'pk_parent':self.profile.pk, 'child_label': LABEL_FOR_CHILD_OBJECT_VOLUNTEERING})

    def save(self, *args, **kwargs):
        manage_instance_ordering(self)
        super().save(*args, **kwargs)


# util functions

def get_website_boostrap_icon(text):
    icon_list = ['github', 'facebook', 'instagram', 'linkedin', 'medium', 'quora', 'reddit', 'skype', 'slack', 'stack-overflow', 'telegram', 'twitch', 'twitter', 'vimeo', 'youtube']

    # use list comprehension!!!
    for index, icon in enumerate(icon_list):
        if icon.replace("-", "") in text:
            return icon_list[index]
    return 'globe'


def get_child_class(child_label):

    if child_label == LABEL_FOR_CHILD_OBJECT_WEBSITE:
        return Website

    if child_label == LABEL_FOR_CHILD_OBJECT_SKILL:
        return Skill

    if child_label == LABEL_FOR_CHILD_OBJECT_LANGUAGE:
        return Language

    if child_label == LABEL_FOR_CHILD_OBJECT_EDUCATION:
        return Education

    if child_label == LABEL_FOR_CHILD_OBJECT_EXPERIENCE:
        return Experience

    if child_label == LABEL_FOR_CHILD_OBJECT_CERTIFICATION:
        return Certification

    if child_label == LABEL_FOR_CHILD_OBJECT_COURSE:
        return Course

    if child_label == LABEL_FOR_CHILD_OBJECT_HONOR:
        return Honor

    if child_label == LABEL_FOR_CHILD_OBJECT_ORGANIZATION:
        return Organization

    if child_label == LABEL_FOR_CHILD_OBJECT_PATENT:
        return Patent

    if child_label == LABEL_FOR_CHILD_OBJECT_PROJECT:
        return Project

    if child_label == LABEL_FOR_CHILD_OBJECT_PUBLICATION:
        return Publication

    if child_label == LABEL_FOR_CHILD_OBJECT_VOLUNTEERING:
        return Volunteering


def update_child_object(child_label=None, child_object=None, request=None):

    if child_label == LABEL_FOR_CHILD_OBJECT_WEBSITE:
        name = request.POST.get("name")
        child_object.name = name
        child_object.bootstrap_icon = get_website_boostrap_icon(str(name))

    if child_label == LABEL_FOR_CHILD_OBJECT_SKILL:
        child_object.name = request.POST.get("name")

    if child_label == LABEL_FOR_CHILD_OBJECT_LANGUAGE:
        child_object.name = request.POST.get("name")
        child_object.level = request.POST.get("level")

    if child_label == LABEL_FOR_CHILD_OBJECT_EDUCATION: # education
        child_object.title = request.POST.get("title")
        child_object.grade = request.POST.get("grade")
        child_object.start_date = request.POST.get("start_date")
        child_object.end_date = request.POST.get("end_date")
        child_object.institution = request.POST.get("institution")
        child_object.institution_link = request.POST.get("institution_link")
        child_object.description = request.POST.get("description")

    if child_label == LABEL_FOR_CHILD_OBJECT_EXPERIENCE:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_CERTIFICATION:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_COURSE:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_HONOR:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_ORGANIZATION:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_PATENT:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_PROJECT:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_PUBLICATION:
        pass

    if child_label == LABEL_FOR_CHILD_OBJECT_VOLUNTEERING:
        pass

    child_object.save()


def set_activation_state(label=None, object=None, active=True):

    if label == LABEL_FOR_PROFILE_FIELD_DESCRIPTION:
        object.description_active = active

    if label == LABEL_FOR_CHILD_OBJECT_WEBSITE:
        object.website_active = active

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


def get_child_object(child_label=None, pk=None, profile=None):
    """
    This function gets an instance object
    """
    Klass = get_child_class(child_label)
    return get_object_or_404(Klass, profile=profile, pk=pk)


def create_empty_child_object(child_label=None, profile=None):
    """
    This function creates an empty object associated with a profile instance
    """
    Klass = get_child_class(child_label)
    return Klass(profile=profile)


def get_above_child_object(child_label=None, child_object=None, profile=None):
    """
    This function gets an instance object that is located before the "child_object"
    """
    Klass = get_child_class(child_label)
    return Klass.objects.filter(order__lt=child_object.order, profile=profile).last()


def get_below_child_object(child_label=None, child_object=None, profile=None):
    """
    This function gets an instance object that is located after the "child_object"
    """
    Klass = get_child_class(child_label)
    return Klass.objects.filter(order__gt=child_object.order, profile=profile).first()
