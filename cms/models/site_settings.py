from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

from ..utils import get_localized_fieldpannels


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
class FooterSlogan(BaseSiteSetting):
    text = models.TextField(blank=True, null=True)

    panels = [
        MultiFieldPanel(
            get_localized_fieldpannels("text"),
            heading="Footer Slogan in Footer",
        )
    ]
