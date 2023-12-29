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
    m.send(fail_silently=True)

    ## check if user has ordered a plan with manual profile creation
    if instance.plan.profile_manual:
        subject_m = "Nice CV | " + _("Send us your actual CV")
        body_m = _(
            """Hi again,
            
Great choice! You have ordered our special plan which includes writing a CV for you.

In order for us to proceed, we need your actual CV. So please send it to us and we will start working on it as soon as possible.

I look forward to your feedback!
"""
        )
        m_m = EmailMessage(
            subject_m, body_m, settings.DEFAULT_FROM_EMAIL, [instance.user.email]
        )
        m_m.send(fail_silently=True)
