from django.db import models

from wagtail.models import Page

from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from ..blocks import ArticleStreamBlock


class BlogIndexPage(Page):
    template = "cms/blog_index.html"

    parent_page_type = ["cms.HomePage"]
    subpage_types = ["cms.BlogPostPage"]


class BlogPostPage(Page):
    template = "cms/blog_post.html"
    parent_page_type = ["cms.BlogIndexPage"]
    subpage_types = ["cms.BlogPostPage"]

    description = models.TextField(
        max_length=1024,
        null=True,
        blank=True,
    )
    body = StreamField(
        ArticleStreamBlock(),
        null=True,
        blank=True,
        use_json_field=True,
        collapsed=False,
    )
    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("body"),
    ]
