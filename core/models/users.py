import datetime

import auto_prefetch
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

from .plans import FreePlan
from .plans import PremiumPlan


class User(AbstractUser):
    avatar_url = models.URLField(null=True, blank=True)
    notify_when_plan_expires = models.BooleanField(default=False)

    @cached_property
    def plan(self):
        """Return a PremiumPlan object if the user has a Premium plan.
        If not, return the only FreePlan instance"""
        user_premium_plan = self.user_premium_plans.filter(
            expires__gte=datetime.date.today()
        ).first()
        if user_premium_plan:
            return user_premium_plan.plan
        return FreePlan.get()

    @cached_property
    def fullname(self):
        return self.first_name + " " + self.last_name

    @cached_property
    def number_of_profiles(self):
        return self.plan.profiles

    @cached_property
    def number_of_cvs(self):
        return self.plan.cvs_per_profile

    def __str__(self) -> str:
        return f"User ({self.username} - {self.email})"


class UserPremiumPlan(auto_prefetch.Model):
    user = auto_prefetch.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_premium_plans",
    )
    plan = auto_prefetch.OneToOneField(
        PremiumPlan, on_delete=models.SET_NULL, null=True
    )
    created = models.DateField(auto_now_add=True)
    starts = models.DateField()
    expires = models.DateField()

    def save(self, *args, **kwargs):
        today = datetime.date.today()
        self.starts = today
        self.expires = today + datetime.timedelta(days=(365.25 / 12) * self.plan.months)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created} - {self.user.email}"