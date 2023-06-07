from apps.plans.factories import PremiumPlanFactory

from django.conf import settings
from django.db.utils import IntegrityError
from apps.tex.models import Tex


def create_initial_objects(plans=False):
    # create 2 plan objects

    if plans:
        PremiumPlanFactory()
        PremiumPlanFactory(price=14, months=6)

    # load tex templates
    # TEX_DIR/<template_type>/<interpreter>/<name>/template.tex

    for type_path in settings.TEX_DIR.iterdir():
        for interpreter_path in type_path.iterdir():
            print(type_path.name + " | " + interpreter_path.name + ":")
            for template_path in interpreter_path.iterdir():
                tex = template_path / "template.tex"
                print("\t" + template_path.name + ":")
                if tex.is_file():
                    template = str(tex).replace(
                        str(tex.parent.parent.parent.parent) + "/", ""
                    )

                    try:
                        Tex.objects.create(
                            template_name=template,
                            name=template_path.name,
                            interpreter=interpreter_path.name,
                            is_cv=True if "cvs" == type_path.name else False,
                        )
                        print("\t\t- " + str(template))
                    except IntegrityError:
                        print(f"\t\t- {template} was already created")
