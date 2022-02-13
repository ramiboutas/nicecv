

from django.db import models




from django_tex.shortcuts import render_to_pdf

from profiles.models import Profile
from texfiles.models import ResumeTemplate
from utils.files import get_tex_template_name, delete_path_file

IMAGE_DIRECTORY = f'files/images'
PDF_DIRECTORY = 'files/pdfs'
IMAGE_FORMAT = 'jpg'


class ResumeFile(models.Model):
    profile = models.ForeignKey(Profile, related_name="resume_files", on_delete=models.CASCADE)
    # texfile = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=IMAGE_DIRECTORY) # , upload_to='files/%Y/%m/%d/'
    pdf_file = models.FileField(null=True , upload_to=PDF_DIRECTORY)
