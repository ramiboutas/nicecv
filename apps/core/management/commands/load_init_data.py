from django.conf import settings

from django.core.management.base import BaseCommand

from apps.plans.factories import PremiumPlanFactory
from apps.tex.models import CvTex
from apps.tex.models import TexProfile
from apps.profiles.models import Profile


class Command(BaseCommand):
    help = "Creates initial objects for the site"

    def handle(self, *args, **options):
        if settings.CREATE_INITIAL_PLAN_OBJECTS:
            PremiumPlanFactory()
            PremiumPlanFactory(price=14, months=6)

        if settings.CREATE_INITIAL_CV_TEX_OBJECTS:
            CvTex.create_initial_objects()

        # Render Profile objects (with category=template) in Tex objects (with is_cv=True)

        for tex_obj in CvTex.objects.all():
            for profile_obj in TexProfile.objects.filter(category="template"):
                tex_obj.render_profile(profile_obj)

        self.stdout.write("Objects created.")
