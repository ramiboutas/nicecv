from django.views.i18n import set_language

from wagtail.models import Locale
from wagtail.models import Page


def switch_language(request):
    if "wagtail_page_id" in request.POST:
        # Wagtail page
        another_locale = Locale.objects.get(language_code=request.POST.get("language"))
        page = Page.objects.get(id=request.POST.get("wagtail_page_id"))
        translated_page = page.get_translation(another_locale)
        post = request.POST.copy()
        post["next"] = translated_page.url
        request.POST = post
    return set_language(request)
