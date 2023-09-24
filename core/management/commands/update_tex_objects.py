from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Tex


class Command(BaseCommand):
    help = "Creates or updates Tex objects"

    def handle(self, *args, **options):
        self.stdout.write("Updating objects...")

        # tex objects
        Tex.update_objects()

        self.stdout.write("Objects Updated.")
