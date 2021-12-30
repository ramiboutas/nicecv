import datetime

from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser

from allauth.account.signals import user_signed_up

class CustomUser(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

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


@receiver(user_signed_up)
def get_social_avatar_url(sociallogin, user, *args, **kwargs):
    if sociallogin:
        if sociallogin.account.provider == 'google':
            avatar_url = sociallogin.account.extra_data['picture']
        user.avatar_url=avatar_url
        user.save()
