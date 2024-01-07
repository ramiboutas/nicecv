from wagtail.models import Page

from ..streams import FullStreamBlock


class FlexPage(Page):
    template = "cms/flexpage.html"
    subpage_types = []
    parent_page_type = ["cms.HomePage"]

    body = FullStreamBlock()
