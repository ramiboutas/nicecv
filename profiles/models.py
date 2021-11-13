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
    name = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
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

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=200)
    level = models.IntegerField(default=50)

    def __str__(self):
        return self.title


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')
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
