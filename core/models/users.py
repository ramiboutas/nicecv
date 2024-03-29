import datetime

import auto_prefetch
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from django.urls import reverse

from .plans import FreePlan
from .plans import PremiumPlan


class User(AbstractUser):
    avatar_url = models.URLField(null=True, blank=True)
    asked_to_verify_email = models.BooleanField(default=False)

    @cached_property
    def plan(self):
        """Return a PremiumPlan object if the user has a Premium plan.
        If not, return the only FreePlan instance"""
        premiumplan = self.user_premium_plans.filter(
            expires__gte=datetime.date.today()
        ).first()
        if premiumplan:
            return premiumplan.plan
        return FreePlan.get()

    @cached_property
    def last_user_plan(self):
        return self.user_premium_plans.last()

    @cached_property
    def delete_account_url(self):
        return reverse("account_delete", kwargs={"id": self.id})

    @cached_property
    def fullname(self):
        return self.first_name + " " + self.last_name

    def __str__(self) -> str:
        return f"User ({self.username} - {self.email})"


class UserPremiumPlan(auto_prefetch.Model):
    user = auto_prefetch.ForeignKey(
        User, related_name="user_premium_plans", on_delete=models.SET_NULL, null=True
    )
    plan = auto_prefetch.ForeignKey(PremiumPlan, on_delete=models.SET_NULL, null=True)
    created = models.DateField(auto_now_add=True)
    starts = models.DateField()
    expires = models.DateField()

    def save(self, *args, **kwargs):
        today = datetime.date.today()
        self.starts = today
        self.expires = today + datetime.timedelta(days=(365.25 / 12) * self.plan.months)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"UserPremiumPlan({self.starts} - {self.expires})"
