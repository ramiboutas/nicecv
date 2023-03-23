import datetime

import auto_prefetch
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.plans.models import PremiumPlan
from apps.plans.models import get_free_plan


class CustomUser(AbstractUser):
    avatar_url = models.URLField(null=True, blank=True)
    notify_when_plan_expires = models.BooleanField(default=False)

    def get_actual_plan(self):
        """Return a PremiumPlan instance if the user has one.
        If not, return the FreePlan instance"""
        user_premium_plan = self.user_premium_plans.filter(
            expires__gte=datetime.date.today()
        ).first()
        if user_premium_plan:
            return user_premium_plan.plan
        return get_free_plan()

    @property
    def number_of_profiles(self):
        return self.get_actual_plan().profiles


class UserPremiumPlan(auto_prefetch.Model):
    user = auto_prefetch.ForeignKey(
        CustomUser,
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
