from django.db import models

from wagtail.models import Page


from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    template = "cms/home.html"
    subtitle = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]
