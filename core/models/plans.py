import auto_prefetch
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class AbractPlan(auto_prefetch.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128, null=True)
    profiles = models.PositiveSmallIntegerField(default=1)
    includes_support = models.BooleanField(default=False)
    profile_translation = models.BooleanField(default=False)
    profile_manual = models.BooleanField(default=False)
    premium_templates = models.BooleanField(default=False)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True


class FreePlan(AbractPlan):
    singleton = models.BooleanField(primary_key=True, default=True)

    class Meta(auto_prefetch.Model.Meta):
        constraints = (
            models.CheckConstraint(
                name="single_free_plan", check=models.Q(singleton=True)
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
        constraints = (
            UniqueConstraint(
                fields=["months"],
                name="unique_months_field",
            ),
            UniqueConstraint(
                fields=("profile_manual",),
                condition=Q(profile_manual=True),
                name="unique_plan_with_manual_profile",
            ),
        )

    @cached_property
    def detail_url(self):
        return reverse("plan_detail", kwargs={"id": self.id})

    @cached_property
    def checkout_url(self):
        return reverse("plan_checkout", kwargs={"id": self.id})
