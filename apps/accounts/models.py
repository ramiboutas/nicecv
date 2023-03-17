import datetime

import auto_prefetch
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.plans.models import PremiumPlan


#  RuntimeWarning: DateTimeField UserPremiumPlan.starts received a naive datetime (2023-03-16 00:00:00) while time zone support is active.
#  RuntimeWarning: DateTimeField UserPremiumPlan.expires received a naive datetime (2023-06-15 00:00:00) while time zone support is active.


class CustomUser(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    def has_active_plan(self):
        if self.paid_until is None:
            return False
        return self.paid_until >= datetime.date.today()

    def get_actual_plan(self):
        # if no actual premium plan -> FreePlan instance
        pass

    def set_plan(self, plan: PremiumPlan):
        self.plan = plan
        today = datetime.date.today()
        extra = datetime.timedelta(days=(365.25 / 12) * plan.months)

        if self.paid_until is None:
            self.paid_until = today + extra

        elif self.paid_until <= today:
            self.paid_until = today + extra

        else:
            self.paid_until = self.paid_until + extra

        self.save()


class UserPremiumPlan(auto_prefetch.Model):
    user = auto_prefetch.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    plan = auto_prefetch.OneToOneField(
        PremiumPlan, on_delete=models.SET_NULL, null=True
    )
    created = models.DateField(auto_now_add=True)
    starts = models.DateField()
    expires = models.DateField()

    def save(self, *args, **kwargs):
        plan_delta_time = datetime.timedelta(days=(365.25 / 12) * self.plan.months)
        if self.user.paid_until:
            self.starts = self.user.paid_until
            self.expires = self.starts + plan_delta_time
        else:
            self.starts = datetime.date.today()
            self.expires = datetime.date.today() + plan_delta_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created} - {self.user.email}"
