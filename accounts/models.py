import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    def has_premium(self):
        if self.paid_until is None:
            return False
        return self.paid_until >= datetime.date.today()

    def set_paid_until(self, months: int):
        today = datetime.date.today()
        extra = datetime.timedelta(days=(365.25/12)*months)
        if self.paid_until is not None:
            if self.paid_until > today:
                self.paid_until = self.paid_until + extra
            else:
                self.paid_until = today + extra
        else:
            self.paid_until = today + extra
        
        self.save()


# @receiver(social_account_added)
# @receiver(user_signed_up)
# def get_social_avatar_url(sociallogin, user, *args, **kwargs):
#     try:
#         if sociallogin:
#             if sociallogin.account.provider == 'google':
#                 avatar_url = sociallogin.account.extra_data['picture']
#             user.avatar_url=avatar_url
#             user.save()
#     except:
#         pass