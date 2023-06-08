from functools import cache


from apps.tex.models import CvTex


@cache
def context_processors(request):
    return {
        "resume_templates": CvTex.objects.filter(is_active=True),
        "request": request,
    }
