from django.core.mail import EmailMessage

from utils.telegram import report_to_admin
from .exceptions import ObjectIsNotAnInstanceOfEmailMessageError


def send_email_message(m: EmailMessage):
    if not isinstance(m, EmailMessage):
        raise ObjectIsNotAnInstanceOfEmailMessageError
    try:
        m.send(fail_silently=False)
    except Exception as e:
        report_to_admin(f"Failed to send email to {m.to}: \n\n {e}")
