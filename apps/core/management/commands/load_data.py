from django.conf import settings

from django.core.management.base import BaseCommand

from apps.plans.factories import PremiumPlanFactory
from apps.tex.models import CvTex
from apps.profiles.models import Profile
from apps.cvs.models import Cv
from apps.core.models import Language


class Command(BaseCommand):
    help = "Creates initial objects for the site"

    def handle(self, *args, **options):
        self.stdout.write("Creating objects...")
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
        Cv.render_profile_templates()

        self.stdout.write("Objects created.")
