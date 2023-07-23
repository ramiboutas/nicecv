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
from wagtail.models import Orderable

from ..blocks import FullStreamBlock


class HomeFeature(Orderable):
    # Add as block???
    page = ParentalKey("cms.HomePage", related_name="features")
    svg = models.ForeignKey(
        "wagtaildocs.Document",
        blank=True,  # or False
        null=True,  # or False
        related_name="+",
        on_delete=models.SET_NULL,  # Only works with null=True
    )

    # panels = [ImageChooserPanel("carousel_image")]


class HomePage(Page):
    template = "cms/home.html"

    # Body section of the HomePage
    body = StreamField(
        FullStreamBlock(),
        verbose_name="Home content block",
        null=True,
        blank=True,
        use_json_field=True,
        collapsed=False,
    )
    content_panels = Page.content_panels + [FieldPanel("body")]

    def __str__(self):
        return self.title


def get_default_homepage():
    try:
        return HomePage.objects.get(locale__language_code=settings.LANGUAGE_CODE)
    except HomePage.DoesNotExist:
        pass
