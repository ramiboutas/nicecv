from datetime import datetime, timedelta

from django.core.management import call_command
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.core.mail import EmailMessage
from django.conf import settings

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task


from .models.profiles import Profile
from .models.users import User


@db_periodic_task(crontab(hour="0", minute="5"))
def update_exchange_rates():
    call_command("update_rates", verbosity=0)


@db_periodic_task(crontab(hour="8", minute="10"))
def notify_to_complete_profile():
    # Get last updated profiles
    profiles = Profile.objects.filter(
        email__isnull=False,
        category__in=("temporal", "user_profile"),
        updated__gt=datetime.now() - timedelta(days=1),
    )
    # Collect emails depending on the profile completion
    profiles_to_email = []
    for p in profiles:
        if not p.has_children_exclude("cv_set"):
            profiles_to_email.append(p)

    # Send emails
    for p in profiles_to_email:
        try:
            activate(p.language)
        except:
            pass
        subject = "Nice CV | " + _("Complete your profile")
        body = _("Hello")
        if p.fullname is not None:
            body += " " + p.fullname
        body += ",\n\n"
        body += _("This is Rami from nicecv.online.")
        body += "\n\n"
        body += _("I am glad you want to improve the aesthetics of your CV.")
        body += "\n\n"
        body += _(
            "I writing to you because it seems that you decided to abandon the process of creating a CV that will impress recruiters."
        )
        body += " "
        body += _(
            "But if you want to complete your profile and download CV templates, visit the site:"
        )
        body += "\n\n"
        body += "https://nicecv.online"
        body += "\n\n"
        body += _("Best wishes, Rami.")

        m = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [p.email])
        m.send(fail_silently=False)


@db_periodic_task(crontab(hour="8", minute="15"))
def ask_to_verify_email():
    from allauth.account.models import EmailAddress

    users = User.objects.none()
    qs = EmailAddress.objects.filter(verified=False, user__asked_to_verify_email=False)

    # qs = asked_to_verify_email
    for obj in qs:
        last_profile = obj.user.profile_set.last()
        if last_profile is not None:
            try:
                activate(last_profile.language)
            except:
                pass
        subject = "Nice CV | " + _("Verify your Email")
        body = _("Hi ") + obj.user.fullname
        body += "\n\n"
        body += _("This is Rami from nicecv.online.")
        body += "\n\n"
        body += _("Please consider to verify your email:")
        body += "\n\n"
        body += _("1. Just visit this page: https://nicecv.online/email/")
        body += "\n\n"
        body += _("2. Click on Re-send Verification")
        body += "\n\n"
        body += _("3. Go to you Email inbox and confirm your Email Address.")
        body += "\n\n"
        body += "Thanks."
        body += "\n\n"
        body += _("Best wishes, Rami.")
        m = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [obj.email])
        m.send(fail_silently=False)
        users = users.union(obj.user)

    users.update(asked_to_verify_email=True)


@db_periodic_task(crontab(hour="0", minute="15"))
def remove_temporal_profiles():
    # Delete all temporal profiles
    Profile.objects.filter(
        category="temporal", updated__lt=datetime.now() - timedelta(days=30)
    ).delete()
    # Delete recent temporal profiles with no fullname and no email
    Profile.objects.filter(
        category="temporal",
        updated__lt=datetime.now() - timedelta(days=1),
        fullname__isnull=True,
        email__isnull=True,
    ).delete()


@db_periodic_task(crontab(hour="0", minute="20"))
def remove_expired_sessions():
    call_command("clearsessions", verbosity=0)
