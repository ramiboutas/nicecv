import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)

    def has_paid(self):
        if self.paid_until == None or self.paid_until == '':
            return False
        return self.paid_until >= datetime.date.today()

    def set_paid_until(self, months: int):
        if self.paid_until != None and self.paid_until != '':
            if self.paid_until > datetime.date.today():
                self.paid_until = self.paid_until + datetime.timedelta(days=(365.25/12)*months)
            else:
                self.paid_until = datetime.date.today() + datetime.timedelta(days=(365.25/12)*months)
        else:
            self.paid_until = datetime.date.today() + datetime.timedelta(days=(365.25/12)*months)
        self.save()
    #
    # def pro_days_left(self):
    #     if self.paid_until == None or self.paid_until == '':
    #         return 0
    #     days = (self.paid_until - datetime.date.today()).days
    #     return days




class EarlyAdopter(models.Model):
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
