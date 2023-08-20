from django.core.management.base import BaseCommand

from ...models.tex import copy_texmf


class Command(BaseCommand):
    help = "Copies latex local files to destination"

    def handle(self, *args, **options):
        copy_texmf()
