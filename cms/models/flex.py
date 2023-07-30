from wagtail.models import Page

from ..blocks import FullStreamBlock


class FlexPage(Page):
    template = "cms/page.html"

    body = FullStreamBlock()
