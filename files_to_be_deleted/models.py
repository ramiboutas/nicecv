from django.db import models

from profiles.models import Profile

IMAGE_DIRECTORY = 'files/images'
PDF_DIRECTORY = 'files/pdfs'
IMAGE_FORMAT = 'jpg'


class ResumeFile(models.Model):
    profile = models.ForeignKey(Profile, related_name="resume_files", on_delete=models.CASCADE)
    # texfile = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=IMAGE_DIRECTORY) # , upload_to='files/%Y/%m/%d/'
    pdf = models.FileField(null=True , upload_to=PDF_DIRECTORY)
