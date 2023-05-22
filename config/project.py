from functools import cache

from django.conf import settings

from apps.tex.models import CoverLetterTemplate
from apps.tex.models import ResumeTemplate


@cache
def context_processors(request):
    return {
        "coverletter_templates": CoverLetterTemplate.objects.filter(is_active=True),
        "resume_templates": ResumeTemplate.objects.filter(is_active=True),
        "html_forms": settings.HTML_FORMS,
        "request": request,
    }
