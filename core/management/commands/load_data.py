from django.conf import settings
from django.core.management.base import BaseCommand

from ...factories.plans import PremiumPlanFactory
from ...models.cvs import Cv
from ...models.deepl_language import DeeplLanguage
from ...models.profiles import Profile
from ...models.tex import Tex


class Command(BaseCommand):
    help = "Creates initial objects for the site"

    def handle(self, *args, **options):
        self.stdout.write("Creating objects...")

        # language objects
        DeeplLanguage.update_objects()

        # plan objects
        PremiumPlanFactory()
        PremiumPlanFactory(price=14, months=6)

        # profile templates
        template_profiles = Profile.create_template_profiles()

        # cv objects
        Cv.objects.filter(profile__auto_created=True).delete()
        for tex in Tex.objects.filter(active=True):
            for profile in template_profiles:
                cv = Cv.objects.create(profile=profile, tex=tex, auto_created=True)
                cv.render_files()
                print(f"✅ {cv} created.")
                del cv

        self.stdout.write("Objects created.")
