from django.conf import settings
from django.views.i18n import set_language
from django.contrib import messages
from django.utils.translation import gettext as _


from wagtail.models import Locale
from wagtail.models import Page


def switch_language(request):
    if "wagtail_page_id" in request.POST:
        # Wagtail page
        page_found = True
        locale_found = True
        post = request.POST.copy()
        lang_code = request.POST.get("language", settings.LANGUAGE_CODE)

        try:
            locale = Locale.objects.get(language_code=lang_code)
        except Locale.DoesNotExist:
            messages.info(request, _("This page does not exist in that language"))
            locale_found = False

        try:
            page = Page.objects.get(id=request.POST.get("wagtail_page_id"))
        except Page.DoesNotExist:
            messages.error(request, _("There was an error with this page"))
            page_found = False
            post["next"] = "/"

        if locale_found and page_found:
            post["next"] = page.get_translation(locale).url

        request.POST = post

    return set_language(request)
