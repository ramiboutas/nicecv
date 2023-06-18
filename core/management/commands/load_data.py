from django.conf import settings
from django.core.management.base import BaseCommand

from ...factories.plans import PremiumPlanFactory
from ...models.tex import copy_latex_local_files_to_destination
from ...models import Cv
from ...models import Profile
from ...models import CvTex
from ...models import Language
from ...models import Secrets


class Command(BaseCommand):
    help = "Creates initial objects for the site"

    def handle(self, *args, **options):
        self.stdout.write("Creating objects...")

        # copy latex local files
        copy_latex_local_files_to_destination()

        # db-based settings
        Secrets.get()
        # language objects
        Language.update_objects()
        # plan objects
        PremiumPlanFactory()
        PremiumPlanFactory(price=14, months=6)

        # tex objects
        CvTex.update_objects()

        # profile templates
        Profile.create_template_profiles()

        # cv objects
        if not getattr(settings, "TEST_MODE", False):
            Cv.crete_cvs_from_profile_templates()

        self.stdout.write("Objects created.")
