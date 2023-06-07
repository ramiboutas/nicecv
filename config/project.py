from functools import cache


from apps.tex.models import Tex


@cache
def context_processors(request):
    return {
        "resume_templates": Tex.objects.filter(is_active=True),
        "request": request,
    }
