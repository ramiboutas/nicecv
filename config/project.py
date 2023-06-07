from functools import cache


from apps.tex.models import ResumeTemplate


@cache
def context_processors(request):
    return {
        "resume_templates": ResumeTemplate.objects.filter(is_active=True),
        "request": request,
    }
