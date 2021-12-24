from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.utils import timezone

import uuid
from PIL import Image
# from croppie.fields import CroppieField

User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.username.id, filename)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project

    # Localizable address that a member wants to display on the profile. Represented as a MultiLocaleString object type.
    address = models.CharField(null=True, blank=True, max_length=120)

    # Birth date of the member. Represented as a date object.
    birthDate = models.DateTimeField(null=True, blank=True)


    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='profiles/', default='profiles/defaultphoto.png') # change later when auth is finneshed
    fullname = models.CharField(max_length=200)
    jobtitle = models.CharField(max_length=200)
    birthdate = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    interests = models.CharField(max_length=200)
    skill_label = models.CharField(max_length=100, default=_('Skills'))
    experience_label = models.CharField(max_length=100, default=_('Work experience'))
    education_label = models.CharField(max_length=100, default=_('Education'))
    publication_label = models.CharField(max_length=100, default=_('Publications'))
    last_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.id} "

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.photo)

        if img.height > 300 or img.width > 300:
            new_size = (300, 300) # image proportion is manteined / we dont need to do extra work
            img.thumbnail(new_size)
            img.save(self.photo.path)


class BackgroundPicture(models.Model):
    """
    Metadata about the member's background image in the profile. This replaces existing backgroundImage.
    See Background Picture Fields for a description of the fields available within this object.
    """
    profile = models.ForeignKey(Profile, related_name='background_picture', on_delete=models.CASCADE)
    linkedin_data = models.JSONField(null=True, blank=True)


class Certification(models.Model):
    """
    An object representing the certifications that the member holds.
    See Certification Fields for a description of the fields available within this object.

    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/certification

    # id 	            Yes The unique identifer of the certification object.
    # startMonthYear 	No 	Start date for the certification. It is a  Date  type. Does not support "day" field.
    # endMonthYear 	    No 	End date for the certification. It is a  Date  type. Does not support "day" field.
    # name 	            No 	Localizable certification name. It is a  MultiLocaleString  type.
    # authority         No 	Localizable name of the certification's issuing body. It is a  MultiLocaleString  type.
    # company 	        No 	Standardized referenced company URN.
    # licenseNumber     No 	Localizable license number for the certification. It is a  MultiLocaleString  type.
    # url 	            No 	External reference to the certification's website or program.

    """
    profile = models.ForeignKey(Profile, related_name='certifications', on_delete=models.CASCADE)
    linkedin_data = models.JSONField(null=True, blank=True) # include all the fields
    linkedin_id = models.BigIntegerField(null=True, blank=True) # maybe not necessary
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=120)
    authority = models.CharField(null=True, blank=True, max_length=120)
    company = models.CharField(null=True, blank=True, max_length=120)
    license = models.CharField(null=True, blank=True, max_length=120)
    url = models.URLField(null=True, blank=True)


class Course(models.Model):
    """
    An object representing courses the member has taken.
    See Course Fields for a description of the fields available within this object.

    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/course
    # id            Yes The unique identifier of the course object.
    # name          No 	Localizable certification name. It is a  MultiLocaleString  type.
    # number 	    No 	Assigned course number. Represented in string.
    # occupation    No 	Member's occupation when the course was completed. Represented as either a standardized referenced company or school URN.
    """
    profile = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
    linkedin_data = models.JSONField(null=True, blank=True)
    linkedin_id = models.BigIntegerField(null=True, blank=True)  # maybe not necessary
    name = models.JSONField(null=True, blank=True)
    number = models.CharField(null=True, blank=True, max_length=120)  # maybe not necessary
    occupation = models.CharField(null=True, blank=True, max_length=120)



class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=200)
    level = models.IntegerField(default=50)

    def __str__(self):
        return self.title


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    begin = models.CharField(max_length=20)
    end = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Publication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    date = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    begin = models.CharField(max_length=20)
    end = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class OtherInfo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='otherinfo')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title
