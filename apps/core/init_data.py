from apps.plans.factories import PremiumPlanFactory

from django.conf import settings
from django.db.utils import IntegrityError
from apps.tex.models import ResumeTemplate


def create_initial_objects(plans=False):
    # create 2 plan objects

    if plans:
        PremiumPlanFactory()
        PremiumPlanFactory(price=14, months=6)

    # load tex templates
    # TEX_DIR/<interpreter>/<name>/template.tex
    # TEX_DIR/<interpreter>/<name>/args.txt ?

    for interpreter_path in settings.TEX_DIR.iterdir():
        print(interpreter_path.name + ":")
        for template_path in interpreter_path.iterdir():
            tex = template_path / "template.tex"
            print("\t" + template_path.name + ":")
            if tex.is_file():
                template = str(tex).replace(str(tex.parent.parent.parent) + "/", "")

                try:
                    ResumeTemplate.objects.create(
                        name=template_path.name,
                        template_name=template,
                        interpreter=interpreter_path.name,
                    )
                    print("\t\t- " + str(template))
                except IntegrityError:
                    print(f"\t\t- {template} was already created")
