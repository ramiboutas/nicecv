import os
import random

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django_tex.core import compile_template_to_pdf
from pdf2image import convert_from_path, convert_from_bytes

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from .models import Profile
from texfiles.models import ResumeTemplate
from .models import Resume
# from utils.files import get_tex_template_name


@shared_task(bind=True)
def create_resume_objects(self, pk=None):
    progress_recorder = ProgressRecorder(self)
    profile = get_object_or_404(Profile, pk=pk)
    resume_template_objects = ResumeTemplate.objects.filter(is_active=True)
    total_resume_templates = resume_template_objects.count()
    # profile = instance.profile

    profile.resumes.all().delete()
    for count, resume_template_object in enumerate(resume_template_objects):
        # get the template name
        # template_name = get_tex_template_name(resume_template_object)
        template_name = resume_template_object.template_name
        context = {'object': profile}

        # create the pdf with django-tex
        bytes_pdf = compile_template_to_pdf(template_name, context)
        pdf = ContentFile(bytes_pdf, f'{_("CV")}_{profile.firstname}_{profile.lastname}_{profile.pk}.pdf')
        resume_file = Resume(profile=profile, pdf=pdf, resume_template=resume_template_object)
        resume_file.save()

        resume_image_dir = os.path.join(settings.MEDIA_ROOT, settings.RESUME_IMAGE_DIRECTORY)
        if not os.path.exists(resume_image_dir):
            os.mkdir(resume_image_dir)

        progress_recorder.set_progress(count+1, total_resume_templates, description=f"{count+1}")

        # convert page cover (in this case) to jpg and save
        resume_image = convert_from_path(
            pdf_path=resume_file.pdf.path,
            dpi=200,
            first_page=1,
            last_page=1,
            fmt='jpg',
            output_folder=resume_image_dir,
            )[0]

        # get name of pdf


        pdf_filename, extension = os.path.splitext(os.path.basename(resume_file.pdf.name))
        new_resume_image_path = '{}.{}'.format(os.path.join(resume_image_dir, pdf_filename), settings.RESUME_IMAGE_FORMAT)
        # rename the file that was saved to be the same as the pdf file
        os.rename(resume_image.filename, new_resume_image_path)
        # get the relative path to the resume image to store in model
        new_resume_image_path_relative = '{}.{}'.format(os.path.join(settings.RESUME_IMAGE_DIRECTORY, pdf_filename), settings.RESUME_IMAGE_FORMAT)
        resume_file.image = new_resume_image_path_relative
        resume_file.save()
