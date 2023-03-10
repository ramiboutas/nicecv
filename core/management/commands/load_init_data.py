from django.core.management.base import BaseCommand

from core.init_data import create_initial_objects

class Command(BaseCommand):
    help = "Publish a random social post that has not been published yet."

    def handle(self, *args, **options):
        create_initial_objects()
        self.stdout.write("Objects created.")


