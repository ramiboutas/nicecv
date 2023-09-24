from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.i18n import set_language
from wagtail.models import Locale
from wagtail.models import Page


def switch_language(request):
    if "wagtail_page_id" in request.POST:
        # Wagtail page
        post = request.POST.copy()
        lang_code = request.POST.get("language", settings.LANGUAGE_CODE)

        try:
            page = Page.objects.get(id=request.POST.get("wagtail_page_id"))
        except (Page.DoesNotExist, ValueError):
            messages.error(
                request,
                _("We did not find the requested page."),
            )
            post["next"] = "/"
            request.POST = post
            return set_language(request)

        try:
            locale = Locale.objects.get(language_code=lang_code)
            post["next"] = page.get_translation(locale).url
        except (Page.DoesNotExist, Locale.DoesNotExist):
            messages.warning(
                request,
                _("Page not available in the requested language."),
            )
            return set_language(request)

        request.POST = post

    return set_language(request)
