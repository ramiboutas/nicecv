from django.core.management.base import BaseCommand


from core.models.countries import Country


class Command(BaseCommand):
    help = "Scrap object from wikipedia and save in the db"

    def handle(self, *args, **options):
        self.stdout.write("Scrapping and saving...")
        Country.scrap_from_wikipedia()
        self.stdout.write("Done!")
