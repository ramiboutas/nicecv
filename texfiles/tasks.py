from celery import shared_task
from celery_progress.backend import ProgressRecorder

from django_htmx.http import trigger_client_event
from django_tex.shortcuts import render_to_pdf
from django_tex.core import compile_template_to_pdf

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from utils.sessions import create_or_get_session_object
from utils.files import get_tex_template_name, generate_zip
from .models import TexFile
from coverletters.models import CoverLetter


@shared_task(bind=True)
def process_download(self, POST_dict, pk):
    progress_recorder = ProgressRecorder(self)

    # getting the coverletter object
    object = get_object_or_404(CoverLetter, pk=pk)
    rows = object.rows.all()

    # getting the tex file with its attributes
    texfile_pk = int(POST_dict.get("texfileselected_pk"))
    texfile_obj = TexFile.objects.get(pk=texfile_pk)
    settings.LATEX_INTERPRETER = texfile_obj.interpreter
    template_name = get_tex_template_name(texfile_obj)

    # getting the data that does not changes
    candidate_name = POST_dict.get("candidate_name").strip()
    candidate_position = POST_dict.get("candidate_position").strip()
    candidate_email = POST_dict.get("candidate_email").strip()
    candidate_phone = POST_dict.get("candidate_phone").strip()
    candidate_location = POST_dict.get("candidate_location").strip()
    candidate_website = POST_dict.get("candidate_website").strip()
    location_date = POST_dict.get("location_date").strip()

    no_changing_context = {'location_date': location_date, 'candidate_name': candidate_name,
    'candidate_position': candidate_position, 'candidate_email': candidate_email, 'candidate_phone': candidate_phone, 'candidate_location':candidate_location,'candidate_website': candidate_website}

    filenames =[]
    files = []
    for index, row in enumerate(rows):
        try:
            filenames.append(f'{index+1}_{_("Application")}_{row.items.all()[1].name}_{row.items.all()[2].name}/{_("coverletter")}.pdf')
        except:
            filenames.append(f'{index+1}_{_("Application")}/{_("coverletter")}.pdf')

    for index, (row, filename) in enumerate(zip(rows, filenames)):
        text = POST_dict.get("text")
        company_text = POST_dict.get("company_text")
        applying_position = POST_dict.get("applying_position")
        applying_position = applying_position.strip()
        for item, column in zip(row.items.all(), object.columns.all()):
            text = text.replace(column.hashtag.name, item.name)
            company_text = company_text.replace(column.hashtag.name, item.name)
            applying_position = applying_position.replace(column.hashtag.name, item.name)

        # text processing
        text_paragraphs = [line for line in text.splitlines() if line]
        company_text = '\r\n'.join(line for line in company_text.splitlines() if line)
        changing_context = {'text_paragraphs': text_paragraphs, 'company_text': company_text, 'applying_position': applying_position}
        context = {**changing_context, **no_changing_context}
        pdf = compile_template_to_pdf(template_name, context)
        files.append((filename, pdf))
        progress_recorder.set_progress(index, len(filenames))


    full_zip_in_memory = generate_zip(files)
    zip_file = ContentFile(full_zip_in_memory, f'{_("coverletters")}_{object.pk}.zip')
    object.zip_file = zip_file
    object.tex_file = texfile_obj
    object.save()
    return "100%"
