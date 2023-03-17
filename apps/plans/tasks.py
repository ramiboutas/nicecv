from celery import Celery
from celery import shared_task
from django.utils.module_loading import import_string
from djmoney import settings


@shared_task(bind=True)
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    # use cron + bash: python manage.py update_rates
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
