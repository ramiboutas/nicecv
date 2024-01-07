from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.models import register_setting
from wagtail.models import Page

from wagtail.images.models import Image

from ..utils import localized_fieldpanel_list
from .text import TextPage


@register_setting(icon="link")
class Links(BaseSiteSetting):
    """Links settings for our custom website."""

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")
    linkedin = models.URLField(blank=True, null=True, help_text="Linkedin URL")
    github = models.URLField(blank=True, null=True, help_text="GitHub URL")
    instagram = models.URLField(blank=True, null=True, help_text="Instagram URL")
    whatsapp = models.URLField(blank=True, null=True, help_text="Whatapp URL")
    telegram = models.URLField(blank=True, null=True, help_text="Telegram URL")
    email = models.EmailField(blank=True, null=True, help_text="Email Address")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("youtube"),
                FieldPanel("linkedin"),
                FieldPanel("instagram"),
                FieldPanel("whatsapp"),
                FieldPanel("telegram"),
                FieldPanel("email"),
            ],
            heading="Links",
        )
    ]


@register_setting(icon="openquote")
class Brand(BaseSiteSetting):
    name = models.CharField(blank=True, null=True, max_length=16)
    svg = models.ForeignKey(
        Image, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    panels = [FieldPanel("name"), FieldPanel("svg")]


@register_setting(icon="user")
class Legal(BaseSiteSetting):
    privacy_policy_page = models.ForeignKey(
        TextPage,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
    )
    terms_page = models.ForeignKey(
        TextPage,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
    )
    impress_page = models.ForeignKey(
        TextPage,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
    )

    panels = (
        localized_fieldpanel_list("privacy_policy_page")
        + localized_fieldpanel_list("terms_page")
        + localized_fieldpanel_list("impress_page")
    )


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
