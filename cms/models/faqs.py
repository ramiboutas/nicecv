from django.db import models

from wagtail.snippets.models import register_snippet
from ..utils import localized_fieldpanel_list

from wagtail.admin.panels import FieldPanel


@register_snippet
class FrequentAskedQuestion(models.Model):
    FAQ_CHOICES = (
        ("pricing", "Related to Pricing"),
        ("featured", "Featured"),
    )
    question = models.CharField(max_length=128)
    answer = models.TextField()
    category = models.CharField(max_length=16, choices=FAQ_CHOICES)
    active = models.BooleanField(default=True)

    panels = (
        [
            FieldPanel("active"),
            FieldPanel("category"),
            # FieldPanel("question"),
            # FieldPanel("answer"),
        ]
        + localized_fieldpanel_list("question")
        + localized_fieldpanel_list("answer")
    )

    def __str__(self) -> str:
        return self.question
