from apps.plans.factories import PremiumPlanFactory

from django.conf import settings
from django.db.utils import IntegrityError
from apps.tex.models import CvTex
from apps.profiles.models import Profile


def read_tex_metadata_attributes(path) -> dict:
    return {}


def create_initial_objects(plans=False):
    # create 2 plan objects

    if plans:
        PremiumPlanFactory()
        PremiumPlanFactory(price=14, months=6)

    # load CV tex templates
    # CV_TEX_DIR/<interpreter>/<name>/template.tex

    for interpreter_path in settings.CV_TEX_DIR.iterdir():
        print(interpreter_path.name + ":")
        for template_path in interpreter_path.iterdir():
            print("\t" + template_path.name + ":")
            tex_path = template_path / "template.tex"
            metadata_path = template_path / "metadata"
            if tex_path.is_file() and metadata_path.is_file():
                template_name = str(tex_path).replace(
                    str(tex_path.parent.parent.parent.parent) + "/", ""
                )
                metadata_attrs = read_tex_metadata_attributes(metadata_path)
                try:
                    CvTex.objects.create(
                        template_name=template_name,
                        interpreter=interpreter_path.name,  # include in metadata
                        name=template_path.name,  # include in metadata
                        **metadata_attrs,
                    )
                    print("\t\t- " + str(template_name))
                except IntegrityError:
                    print(f"\t\t- {template_name} was already created")

    # Render Profile objects (with category=template) in Tex objects (with is_cv=True)
    for tex_obj in CvTex.objects.filter(is_cv=True):
        for profile_obj in Profile.objects.filter(category="template"):
            tex_obj.render_profile(profile_obj)
