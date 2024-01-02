from datetime import datetime, timedelta

from django.core.management import call_command
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.core.mail import EmailMessage
from django.conf import settings

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task


from .models.profiles import Profile


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
        if not p.has_children:
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
        body += _(
            "This is Rami from nicecv.online. I am glad that you have started to take steps to improve the structure and aesthetics of your CV."
        )
        body += "\n\n"
        body += _(
            "Unfortunately, your profile is incomplete. It seems that you have decided to abandon the process of creating a CV that will impress recruiters."
        )
        body += "\n\n"
        body += _(
            "But if you want to complete your profile and download CV templates, visit the site:"
        )
        body += "\n\n"
        body += "https://nicecv.online"
        body += "\n\n"
        body += _("Best wishes, Rami.")

        m = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [p.email])
        m.send(fail_silently=False)


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
