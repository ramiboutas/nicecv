from __future__ import annotations

from functools import cache

from core.models.cvs import Cv


@cache
def context_processors(request):
    return {
        "resume_templates": Cv.objects.filter(
            profile__category="template",
            profile__language_code=request.LANGUAGE_CODE,
        ),
        "request": request,
    }
