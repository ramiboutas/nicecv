from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.admin.panels import FieldRowPanel
from wagtail.admin.panels import InlinePanel
from modelcluster.fields import ParentalKey


class ContactFormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class ContactPage(AbstractEmailForm):
    template = "contact/contact_page.html"

    intro = RichTextField(blank=True)
    trank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label=_("Form fields")),
        FieldPanel("trank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address"),
                        FieldPanel("to_address"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading=_("Email settings "),
        ),
    ]
