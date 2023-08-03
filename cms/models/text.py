from wagtail.models import Page

from wagtail.fields import StreamField

from ..streams import TextStreamBlock
from wagtail.admin.panels import FieldPanel


class TextPage(Page):
    template = "cms/page.html"

    body = StreamField(
        TextStreamBlock(
            features=[
                "h1",
                "h2",
                "h3",
                "h4",
                "italic",
                "bold",
                "ul",
                "ol",
                "link",
                "document-link",
            ]
        ),
        verbose_name="Home content block",
        null=True,
        blank=True,
        use_json_field=True,
        collapsed=False,
    )
    content_panels = Page.content_panels + [FieldPanel("body")]
