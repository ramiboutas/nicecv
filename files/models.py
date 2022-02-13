from django.db import models

from profiles.models import Profile
from texfiles.models import ResumeTemplate

class ResumeFile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    texfile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    image = models.ImageField()
    pdf = models.FileField()
