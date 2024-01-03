from wagtail.models import Page

from ..streams import FullStreamBlock


class FlexPage(Page):
    template = "cms/flexpage.html"

    body = FullStreamBlock()
