from django.conf import settings
from django.core.management.base import BaseCommand

from cms.models import PureDjangoPage


class Command(BaseCommand):
    help = "Creates initial objects for the site"

    def handle(self, *args, **options):
        self.stdout.write("Creating objects...")

        # creating some core pages available in Wagtail
        PureDjangoPage.update_objects()

        self.stdout.write("Objects created.")
