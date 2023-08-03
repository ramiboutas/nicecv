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

from ..streams import FullStreamBlock


class HomePage(Page):
    template = "cms/page.html"

    subpage_types = [
        "cms.BlogIndexPage",
        "cms.TextPage",
        "cms.FlexPage",
    ]

    parent_page_type = ["wagtailcore.Page"]

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
