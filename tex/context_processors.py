from .models import CoverLetterTemplate
from .models import ResumeTemplate


def tex_objects(request):
    return {
        "coverletter_templates": CoverLetterTemplate.objects.filter(is_active=True),
        "resume_templates": ResumeTemplate.objects.filter(is_active=True),
        "request": request,
    }
