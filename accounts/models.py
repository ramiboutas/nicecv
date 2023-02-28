from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import datetime
from django.utils.timezone import timedelta


class CustomUser(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    def has_paid(self):
        if self.paid_until is None:
            return False
        return self.paid_until >= datetime.today()

    def set_paid_until(self, months: int):
        self.paid_until = datetime.today() + timedelta(days=(365.25 / 12) * months)
        self.save()
