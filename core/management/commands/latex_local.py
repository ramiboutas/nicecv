from django.core.management.base import BaseCommand

from ...models.tex import copy_latex_local_files_to_destination


class Command(BaseCommand):
    help = "Copies latex local files to destination"

    def handle(self, *args, **options):
        copy_latex_local_files_to_destination()
