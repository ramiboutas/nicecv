from django.core.management import call_command


from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task


@db_periodic_task(crontab(hour="0", minute="5"))
def update_exchange_rates():
    call_command("update_rates", verbosity=0)
