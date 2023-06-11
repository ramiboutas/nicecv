from __future__ import annotations
from functools import cache


from core.models.cvs import Cv
from core.models.languages import Language


@cache
def context_processors(request):
    return {
        "resume_templates": Cv.objects.filter(
            profile__category="template",
            profile__language_setting=Language.get(request.LANGUAGE_CODE),
        ),
        "request": request,
    }
