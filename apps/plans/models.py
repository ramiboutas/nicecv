import auto_prefetch
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


class AbractPlan(auto_prefetch.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=64, null=True)
    profiles = models.PositiveSmallIntegerField(default=5)
    coverletters = models.PositiveSmallIntegerField(default=10)
    support = models.BooleanField(default=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


@register_snippet
class FreePlan(AbractPlan):
    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("profiles"),
        FieldPanel("coverletters"),
        FieldPanel("support"),
    ]

    def clean(self):
        if self.__class__.objects.count() > 0 and self._state.adding:
            raise ValidationError(_("Only one instance is allowed"))

    class Meta(auto_prefetch.Model.Meta):
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_single_instance",
                check=models.Q(id=1),
            ),
        ]


@register_snippet
class PremiumPlan(AbractPlan):
    months = models.PositiveSmallIntegerField()
    price = MoneyField(max_digits=6, decimal_places=2, default_currency="EUR")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("name_es"),
        FieldPanel("description_es"),
        FieldPanel("name_de"),
        FieldPanel("description_de"),
        FieldPanel("months"),
        FieldPanel("profiles"),
        FieldPanel("coverletters"),
        FieldPanel("price"),
        FieldPanel("support"),
    ]

    def __str__(self):
        return f"{self.months} months"

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("months", "price")
        constraints = [
            UniqueConstraint(fields=["months"], name="unique_months_field"),
        ]

    @property
    def detail_url(self):
        return reverse("plans:detail", kwargs={"id": self.id})

    @property
    def checkout_url(self):
        return reverse("plans:checkout", kwargs={"id": self.id})


@register_snippet
class PlanFAQ(auto_prefetch.Model):
    # Frequent asked question regared to plans
    question = models.CharField(max_length=128)
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


def get_free_plan():
    try:
        plan = FreePlan.objects.get(id=1)
    except FreePlan.DoesNotExist:
        plan = FreePlan.objects.create(
            name="Free Plan", description=_("Enjoy the free plan")
        )
    except IntegrityError:
        plan = FreePlan.objects.all().first()

    return plan


free_plan_instance = get_free_plan()
