from django.views.i18n import set_language
from django.contrib import messages
from django.utils.translation import gettext as _


from wagtail.models import Locale
from wagtail.models import Page


def switch_language(request):
    if "wagtail_page_id" in request.POST:
        # Wagtail page
        post = request.POST.copy()
        try:
            another_locale = Locale.objects.get(
                language_code=request.POST.get("language")
            )
        except Locale.DoesNotExist:
            messages.info(request, _("This page does not exist in that language"))
            return set_language(request)
        try:
            page = Page.objects.get(id=request.POST.get("wagtail_page_id"))
        except Page.DoesNotExist:
            messages.error(request, _("There was an error with this page"))
            post["next"] = "/"

        translated_page = page.get_translation(another_locale)
        if translated_page:
            post["next"] = translated_page.url

        request.POST = post

    return set_language(request)
