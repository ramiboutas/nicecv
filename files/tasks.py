import os

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django_tex.core import compile_template_to_pdf
from pdf2image import convert_from_path, convert_from_bytes

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from profiles.models import Profile
from texfiles.models import ResumeTemplate
from files.models import ResumeFile
from utils.files import get_tex_template_name

IMAGE_DIRECTORY = f'files/images'
PDF_DIRECTORY = 'files/pdfs'
IMAGE_FORMAT = 'jpg'

@shared_task(bind=True)
def create_resume_file_objects(self, pk=None):
    progress_recorder = ProgressRecorder(self)
    profile = get_object_or_404(Profile, pk=pk)
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
























# @shared_task(bind=True)
# def process_download(self, POST_dict, pk):
#     progress_recorder = ProgressRecorder(self)
#
#     # getting the coverletter object
#     object = get_object_or_404(CoverLetter, pk=pk)
#     rows = object.rows.all()
#
#     # getting the tex file with its attributes
#     texfile_pk = int(POST_dict.get("texfileselected_pk"))
#     texfile_obj = TexFile.objects.get(pk=texfile_pk)
#     settings.LATEX_INTERPRETER = texfile_obj.interpreter
#     template_name = get_tex_template_name(texfile_obj)
#
#     # getting the data that does not changes
#     candidate_name = POST_dict.get("candidate_name").strip()
#     candidate_position = POST_dict.get("candidate_position").strip()
#     candidate_email = POST_dict.get("candidate_email").strip()
#     candidate_phone = POST_dict.get("candidate_phone").strip()
#     candidate_location = POST_dict.get("candidate_location").strip()
#     candidate_website = POST_dict.get("candidate_website").strip()
#     location_date = POST_dict.get("location_date").strip()
#
#     no_changing_context = {'location_date': location_date, 'candidate_name': candidate_name,
#     'candidate_position': candidate_position, 'candidate_email': candidate_email, 'candidate_phone': candidate_phone, 'candidate_location':candidate_location,'candidate_website': candidate_website}
#
#     filenames =[]
#     files = []
#     for index, row in enumerate(rows):
#         try:
#             filenames.append(f'{index+1}_{_("Application")}_{row.items.all()[1].name}_{row.items.all()[2].name}/{_("coverletter")}.pdf')
#         except:
#             filenames.append(f'{index+1}_{_("Application")}/{_("coverletter")}.pdf')
#
#     for index, (row, filename) in enumerate(zip(rows, filenames)):
#         text = POST_dict.get("text")
#         company_text = POST_dict.get("company_text")
#         applying_position = POST_dict.get("applying_position")
#         applying_position = applying_position.strip()
#         for item, column in zip(row.items.all(), object.columns.all()):
#             text = text.replace(column.hashtag.name, item.name)
#             company_text = company_text.replace(column.hashtag.name, item.name)
#             applying_position = applying_position.replace(column.hashtag.name, item.name)
#
#         # text processing
#         text_paragraphs = [line for line in text.splitlines() if line]
#         company_text = '\r\n'.join(line for line in company_text.splitlines() if line)
#         changing_context = {'text_paragraphs': text_paragraphs, 'company_text': company_text, 'applying_position': applying_position}
#         context = {**changing_context, **no_changing_context}
#         pdf = compile_template_to_pdf(template_name, context)
#         files.append((filename, pdf))
#         progress_recorder.set_progress(index, len(filenames))
#
#
#     full_zip_in_memory = generate_zip(files)
#     zip_file = ContentFile(full_zip_in_memory, f'{_("coverletters")}_{object.pk}.zip')
#     object.zip_file = zip_file
#     object.tex_file = texfile_obj
#     object.save()
#     return "100%"
