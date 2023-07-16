from wagtail.admin.panels import FieldPanel

from django.conf import settings


def get_localized_fieldpannels(field_name: str):
    return [
        FieldPanel(field_name + "_" + lang[0])
        for lang in settings.WAGTAIL_CONTENT_LANGUAGES
    ]
