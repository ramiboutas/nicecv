from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.core.mail import EmailMessage
from django.conf import settings

from .models.users import UserPremiumPlan


@receiver(post_save, sender=UserPremiumPlan)
def send_welcome_email(sender, instance, created, **kwargs):
    subject = "Nice CV | " + _("Welcome")
    body = _(
        """Hi,
        
Thank you for your order!

Remember that if you have any questions or you require any technical support, you can contact me directly to this email!

Best wishes!
Rami (nicecv.online)
"""
    )
    m = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [instance.user.email])
    m.send(fail_silently=False)
