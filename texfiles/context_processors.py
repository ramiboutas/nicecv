from django.conf import settings

from .models import CoverLetterTemplate, ResumeTemplate


def texfiles(request):
    return {
        'coverletter_templates': CoverLetterTemplate.objects.filter(is_active=True),
        'resume_templates': ResumeTemplate.objects.filter(is_active=True),
        'request': request
    }
