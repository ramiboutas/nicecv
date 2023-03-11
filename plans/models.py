import auto_prefetch
from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from djmoney.models.fields import MoneyField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Plan(auto_prefetch.Model):
    name = models.CharField(max_length=16)
    months = models.PositiveSmallIntegerField()
    max_profiles = models.PositiveSmallIntegerField(default=5)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency="EUR")

    panels = [
        FieldPanel("name"),
        FieldPanel("name_es"),
        FieldPanel("name_de"),
        FieldPanel("months"),
        FieldPanel("max_profiles"),
        FieldPanel("price"),
    ]

    def __str__(self):
        return f"{self.months} months"

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("months", "price")
        constraints = [
            UniqueConstraint(fields=["months"], name="unique_months_field"),
        ]


@register_snippet
class PlanFAQ(auto_prefetch.Model):
    # Frequent asked question regared to plans
    question = models.CharField(max_length=16)
    answer = models.TextField()
    active = models.BooleanField(default=True)

    panels = [
        FieldPanel("active"),
        FieldPanel("question"),
        FieldPanel("answer"),
        FieldPanel("question_es"),
        FieldPanel("answer_es"),
        FieldPanel("question_de"),
        FieldPanel("answer_de"),
    ]

    def __str__(self) -> str:
        return self.question


class Order(auto_prefetch.Model):
    plan = auto_prefetch.ForeignKey(Plan, on_delete=models.CASCADE)
    user = auto_prefetch.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created} - {self.user.email}"
