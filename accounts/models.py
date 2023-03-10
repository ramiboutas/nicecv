import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from plans.models import Plan


class CustomUser(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)
    actual_plan = models.OneToOneField(
        Plan, null=True, blank=True, on_delete=models.SET_NULL
    )

    def has_active_plan(self):
        if self.paid_until is None:
            return False
        return self.paid_until >= datetime.date.today()

    def set_plan(self, plan: Plan):
        self.actual_plan = plan
        today = datetime.date.today()
        extra = datetime.timedelta(days=(365.25 / 12) * plan.months)

        if self.paid_until is None:
            self.paid_until = today + extra

        elif self.paid_until <= today:
            self.paid_until = today + extra

        else:
            self.paid_until = self.paid_until + extra

        self.save()
