from functools import cache

from .models.cvs import Cv


@cache
def cv_templates(request):
    return {
        "cv_templates": Cv.objects.filter(
            profile__category="template",
            profile__language_code=request.LANGUAGE_CODE,
        ),
        "request": request,
    }
