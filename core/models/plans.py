import auto_prefetch
from djmoney.models.fields import MoneyField

from django.conf import settings
from django.db.models import UniqueConstraint
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property


class AbractPlan(auto_prefetch.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=64, null=True)
    profiles = models.PositiveSmallIntegerField(default=1)
    cvs_per_profile = models.PositiveSmallIntegerField(default=5)
    support = models.BooleanField(default=False)
    profile_translation = models.BooleanField(default=False)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


class FreePlan(AbractPlan):
    singleton = models.BooleanField(primary_key=True, default=True)
    name = models.CharField(max_length=32, default="Free Plan")

    class Meta:
        constraints = (
            models.CheckConstraint(
                name="single_free_plan",
                check=models.Q(singleton=True),
            ),
        )

    @classmethod
    def get(cls):
        return cls.objects.get_or_create(singleton=True)[0]


class PremiumPlan(AbractPlan):
    months = models.PositiveSmallIntegerField()
    price = MoneyField(max_digits=6, decimal_places=2, default_currency="EUR")

    def __str__(self):
        return f"{self.months} months"

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("months", "price")
        constraints = [
            UniqueConstraint(fields=["months"], name="unique_months_field"),
        ]

    @cached_property
    def detail_url(self):
        return reverse("plans:detail", kwargs={"id": self.id})

    @cached_property
    def checkout_url(self):
        return reverse("plans:checkout", kwargs={"id": self.id})


class PlanFAQ(auto_prefetch.Model):
    # Frequent asked question regared to plans
    question = models.CharField(max_length=128)
    answer = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.question
