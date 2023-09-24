from django.conf import settings
from wagtail.admin.panels import FieldPanel


def localized_fieldpanel_list(field_name: str):
    return [
        FieldPanel(field_name + "_" + lang[0])
        for lang in settings.WAGTAIL_CONTENT_LANGUAGES
    ]
