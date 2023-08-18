from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from django.core.mail import EmailMessage
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string
