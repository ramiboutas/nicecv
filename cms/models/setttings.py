from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.models import register_setting
from wagtail.models import Page

from wagtail.images.models import Image


from ..utils import localized_fieldpanel_list


@register_setting(icon="link")
class SocialMediaLinks(BaseSiteSetting):
    """Social media settings for our custom website."""

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")
    linkedin = models.URLField(blank=True, null=True, help_text="Linkedin URL")
    github = models.URLField(blank=True, null=True, help_text="GitHub URL")
    instagram = models.URLField(blank=True, null=True, help_text="Instagram URL")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("youtube"),
                FieldPanel("linkedin"),
                FieldPanel("instagram"),
            ],
            heading="Social Media Settings",
        )
    ]


@register_setting(icon="openquote")
class Brand(BaseSiteSetting):
    footer_text = models.TextField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=16)
    svg = models.ForeignKey(
        Image, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    svg_footer = models.ForeignKey(
        Image, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("svg"),
        FieldPanel("svg_footer"),
        MultiFieldPanel(
            localized_fieldpanel_list("footer_text"),
            heading="Footer Slogan in Footer",
        ),
    ]


@register_setting(icon="pick")
class Banner(BaseSiteSetting):
    linked_page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
    )
    title = models.CharField(max_length=32, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
