from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import FieldRowPanel
from wagtail.admin.panels import InlinePanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.admin.panels import PublishingPanel
from wagtail.fields import RichTextField
from wagtail.fields import StreamField
from wagtail.models import Page

from ..blocks import CustomStreamBlock


class HomePage(Page):
    template = "cms/home.html"

    # Hero section of HomePage
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    hero_text = models.CharField(
        max_length=255,
        null=True,
        help_text="Write an introduction",
    )
    hero_cta = models.CharField(
        verbose_name="Hero CTA",
        null=True,
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    # Body section of the HomePage
    body = StreamField(
        CustomStreamBlock(),
        verbose_name="Home content block",
        null=True,
        blank=True,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_cta"),
                        FieldPanel("hero_cta_link"),
                    ]
                ),
            ],
            heading="Hero section",
        ),
    ]

    def __str__(self):
        return self.title


def get_default_homepage():
    try:
        return HomePage.objects.get(locale__language_code=settings.LANGUAGE_CODE)
    except HomePage.DoesNotExist:
        pass
