import os
import uuid
from io import BytesIO
from PIL import Image

from django.core.files.base import ContentFile
from django.core.files import File
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse, reverse_lazy


User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.username.id, filename)


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
    description_visible = models.IntegerField(default=True)
    interests = models.CharField(null=True, blank=True, max_length=200)

    # labels
    skill_label = models.CharField(max_length=100, default=_('Skills'))
    position_label = models.CharField(max_length=100, default=_('Work experience'))
    education_label = models.CharField(max_length=100, default=_('Education'))
    publication_label = models.CharField(max_length=100, default=_('Publications'))
    project_label = models.CharField(max_length=100, default=_('Projects'))
    project_label = models.CharField(max_length=100, default=_('Publications'))


    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

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

    def save_general_and_contact_info_url(self):
        return reverse('profiles_save_general_and_contact_info', kwargs={'pk':self.pk})

    def add_website_object_url(self):
        return reverse('profiles_add_website_object', kwargs={'pk':self.pk})

    def add_skill_object_url(self):
        return reverse('profiles_add_skill_object', kwargs={'pk':self.pk})

    def add_language_object_url(self):
        return reverse('profiles_add_language_object', kwargs={'pk':self.pk})

    def add_description_url(self):
        return reverse('profiles_add_description', kwargs={'pk':self.pk})

    def update_description_url(self):
        return reverse('profiles_update_description', kwargs={'pk':self.pk})

    def delete_description_url(self):
        return reverse('profiles_delete_description', kwargs={'pk':self.pk})

    def add_add_description_button_url(self):
        return reverse('profiles_add_add_description_button', kwargs={'pk':self.pk})

    def delete_add_description_button_url(self):
        return reverse('profiles_delete_add_description_button', kwargs={'pk':self.pk})

    def add_education_object_url(self):
        return reverse('profiles_add_education_object', kwargs={'pk':self.pk})

    def add_education_new_form_url(self):
        return reverse('profiles_add_education_new_form', kwargs={'pk':self.pk})

    def delete_education_new_form_url(self):
        return reverse('profiles_delete_education_new_form', kwargs={'pk':self.pk})

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
        return reverse('profiles_update_website_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})

    def delete_object_url(self):
        return reverse('profiles_delete_website_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})


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
        return reverse('profiles_update_skill_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})

    def delete_object_url(self):
        return reverse('profiles_delete_skill_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})


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
        return reverse('profiles_update_language_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})

    def delete_object_url(self):
        return reverse('profiles_delete_language_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})


class Education(models.Model):
    """
    An object representing the member's educational background.
    See Education Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/education
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education_set')
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    grade = models.CharField(null=True, blank=True, max_length=20)
    title = models.CharField(null=True, blank=True, max_length=100)
    subtitle = models.CharField(null=True, blank=True, max_length=100)
    institution = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=300)

    def __str__(self):
        return self.degree_name

    def update_object_url(self):
        return reverse('profiles_update_education_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})

    def delete_object_url(self):
        return reverse('profiles_delete_education_object', kwargs={'pk':self.pk, 'pk_parent':self.profile.pk})


class Certification(models.Model):
    """
    An object representing the certifications that the member holds.
    See Certification Fields for a description of the fields available within this object.
    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/certification
    """
    profile = models.ForeignKey(Profile, related_name='certifications', on_delete=models.CASCADE)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    name = models.CharField(null=True, blank=True, max_length=100)
    authority = models.CharField(null=True, blank=True, max_length=100)
    company = models.CharField(null=True, blank=True, max_length=100)
    license = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)


class Course(models.Model):
    """
    An object representing courses the member has taken.
    See Course Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/course
    """
    profile = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
    name = models.JSONField(null=True, blank=True)
    number = models.CharField(null=True, blank=True, max_length=100)
    occupation = models.CharField(null=True, blank=True, max_length=100)




class Honor(models.Model):
    """
    An object representing the various honors and awards the member has received.
    See Honor Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/honor
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='honors')
    title = models.CharField(null=True, blank=True, max_length=100)
    issue_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)


class OrganizationMember(models.Model):
    """
    An object representing the organizations that the member is in.
    See Organization Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/organization
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organizations')
    linkedin_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    position = models.CharField(null=True, blank=True, max_length=100)


class Patent(models.Model):
    """
    An object representing the various patents associated with the member.
    See Patent Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/patent
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patents')
    linkedin_id = models.BigIntegerField(null=True, blank=True)
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



class Position(models.Model):
    """
    Employment history. See Positions for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    company_name = models.CharField(null=True, blank=True, max_length=100)
    location_name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    members = models.CharField(null=True, blank=True, max_length=200)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    ongoing = models.BooleanField(null=True, blank=True) # singleDate
    issuer = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class Publication(models.Model):
    """
    An object representing the various publications associated with the member.
    See Publication Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    name = models.CharField(null=True, blank=True, max_length=200)
    date = models.CharField(null=True, blank=True, max_length=20)
    description = models.TextField(null=True, blank=True, max_length=1000)
    authors = models.CharField(null=True, blank=True, max_length=200)
    publisher = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name





class VolunteeringExperience(models.Model):
    """
    An object representing the member's volunteering experience.
    See Volunteering Experience Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/volunteering-experience
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='volunteering_experiences')
    title = models.CharField(null=True, blank=True, max_length=100)
    role = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)
    cause = models.CharField(null=True, blank=True, max_length=100)
    ongoing = models.BooleanField(null=True, blank=True) # singleDate
