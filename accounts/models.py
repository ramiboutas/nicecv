import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)

    def has_paid(self):
        if self.paid_until is None or self.paid_until is '':
            return False
        return self.paid_until >= datetime.date.today()

    def set_paid_until(self, months: int):
        self.paid_until = datetime.date.today() + datetime.timedelta(days=(365.25/12)*months)
        self.save()
