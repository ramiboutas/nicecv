from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from ..streams import TextStreamBlock
from django.conf import settings


class TextPage(Page):
    template = "cms/textpage.html"

    subpage_types = []
    parent_page_type = ["cms.HomePage"]

    body = StreamField(
        TextStreamBlock(features=settings.CMS_RICHTEXT_FEATURES),
        verbose_name="Home content block",
        null=True,
        blank=True,
        use_json_field=True,
        collapsed=False,
    )
    content_panels = Page.content_panels + [FieldPanel("body")]
