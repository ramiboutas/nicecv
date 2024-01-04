from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.core.mail import EmailMessage
from django.conf import settings

from .models.users import UserPremiumPlan, User
from .models.plans import PremiumPlan
from .email import send_email_message


from djstripe.models import Event


@receiver(post_save, sender=Event)
def process_stripe_event(sender, instance, created, **kwargs):
    proceed = (
        instance.type == "checkout.session.completed"
        and "plan_id"
        and "user_id" in instance.data["object"]["metadata"]
    )

    if not proceed:
        return

    plan_id = int(instance.data["object"]["metadata"]["plan_id"])
    user_id = int(instance.data["object"]["metadata"]["user_id"])

    try:
        user = User.objects.get(id=user_id)
        plan = PremiumPlan.objects.get(id=plan_id)
    except (User.DoesNotExist, PremiumPlan.DoesNotExist):
        return

    userplan = UserPremiumPlan.objects.create(plan=plan, user=user)

    subject = "Nice CV | " + _("Welcome")
    body = _(
        """Hi,
        
Thank you for your order!

Remember that if you have any questions or you require any technical support, you can contact me directly to this email!

Best wishes!
Rami (nicecv.online)
"""
    )
    m = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [userplan.user.email])
    # m.send(fail_silently=True)
    send_email_message(m)

    ## check if user has ordered a plan with manual profile creation
    if userplan.plan.profile_manual:
        subject_m = "Nice CV | " + _("Send us your actual CV")
        body_m = _(
            """Hi again,
            
Great choice! You have ordered our special plan which includes writing a CV for you.

In order for us to proceed, we need your actual CV. So please send it to us and we will start working on it as soon as possible.

I look forward to your feedback!
"""
        )
        m_m = EmailMessage(
            subject_m, body_m, settings.DEFAULT_FROM_EMAIL, [userplan.user.email]
        )
        # m_m.send(fail_silently=True)
        send_email_message(m_m)
