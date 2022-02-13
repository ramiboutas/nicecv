import os
from datetime import datetime
from django_tex.core import compile_template_to_pdf
from pdf2image import convert_from_path, convert_from_bytes

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django_tex.shortcuts import render_to_pdf

from profiles.models import Profile, Skill, Language, Education, Experience, Certification, Course, Honor, Organization, Patent, Project, Publication, Volunteering
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


def create_resume_file_objects(profile=None):
    resume_template_objects = ResumeTemplate.objects.filter(is_active=True)
    # profile = instance.profile
    profile.resume_files.all().delete()
    for resume_template_object in resume_template_objects:
        # get the template name
        template_name = get_tex_template_name(resume_template_object)
        context = {'object': profile}
        # create the pdf with django-tex
        pdf_file_in_memory = compile_template_to_pdf(template_name, context)
        pdf_file = ContentFile(pdf_file_in_memory, f'{_("CV")}_{profile.pk}_{resume_template_object.pk}.pdf')
        resume_file = ResumeFile(profile=profile, pdf_file=pdf_file)
        resume_file.save()

        resume_image_dir = os.path.join(settings.MEDIA_ROOT, IMAGE_DIRECTORY)
        if not os.path.exists(resume_image_dir):
            os.mkdir(resume_image_dir)

        # convert page cover (in this case) to jpg and save
        resume_image = convert_from_path(
            pdf_path=resume_file.pdf_file.path,
            dpi=200,
            first_page=1,
            last_page=1,
            fmt='jpg',
            output_folder=resume_image_dir,
            )[0]

        # get name of pdf_file
        pdf_filename, extension = os.path.splitext(os.path.basename(resume_file.pdf_file.name))
        new_resume_image_path = '{}.{}'.format(os.path.join(resume_image_dir, pdf_filename), IMAGE_FORMAT)
        # rename the file that was saved to be the same as the pdf file
        os.rename(resume_image.filename, new_resume_image_path)
        # get the relative path to the resume image to store in model
        new_resume_image_path_relative = '{}.{}'.format(os.path.join(IMAGE_DIRECTORY, pdf_filename), IMAGE_FORMAT)
        resume_file.image = new_resume_image_path_relative
        resume_file.save()


@receiver(post_delete, sender=Skill)
@receiver(post_save, sender=Skill)
@receiver(post_delete, sender=Language)
@receiver(post_save, sender=Language)
@receiver(post_delete, sender=Education)
@receiver(post_save, sender=Education)
@receiver(post_delete, sender=Experience)
@receiver(post_save, sender=Experience)
@receiver(post_delete, sender=Certification)
@receiver(post_save, sender=Certification)
@receiver(post_delete, sender=Course)
@receiver(post_save, sender=Course)
@receiver(post_delete, sender=Honor)
@receiver(post_save, sender=Honor)
@receiver(post_delete, sender=Organization)
@receiver(post_save, sender=Organization)
@receiver(post_delete, sender=Patent)
@receiver(post_save, sender=Patent)
@receiver(post_delete, sender=Project)
@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Publication)
@receiver(post_save, sender=Publication)
@receiver(post_delete, sender=Volunteering)
@receiver(post_save, sender=Volunteering)
@receiver(post_save, sender=Profile)
def file_education_trigger(sender, instance, **kwargs):
    if sender == Profile:
        create_resume_file_objects(profile=instance)
    else:
        create_resume_file_objects(profile=instance.profile)



@receiver(post_delete, sender=ResumeFile)
def delete_resume_files(sender, instance, **kwargs):
    if instance.image:
        delete_path_file(instance.image.path)
    if instance.pdf_file:
        delete_path_file(instance.pdf_file.path)
