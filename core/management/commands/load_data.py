from django.conf import settings

from django.core.management.base import BaseCommand

from ...factories.plans import PremiumPlanFactory
from ...models.tex import CvTex
from ...models.profiles import Profile
from ...models.cvs import Cv

from core.models.languages import Language
from core.models.secrets import Secrets


class Command(BaseCommand):
    help = "Creates initial objects for the site"

    def handle(self, *args, **options):
        self.stdout.write("Creating objects...")
        # db-based settings
        Secrets.get()  # this gets
        # language objects
        Language.create_initial_objects()
        # plan objects
        PremiumPlanFactory()
        PremiumPlanFactory(price=14, months=6)
        # cv tex objects
        CvTex.update_objects()

        # profile templates
        Profile.create_template_profiles()

        # cv objects
        Cv.crete_cvs_from_profile_templates()

        self.stdout.write("Objects created.")
