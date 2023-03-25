from django.db import transaction


from . import forms
from . import models


@transaction.atomic
def create_initial_profile(request) -> models.Profile:
    # create an empty profile
    profile = models.Profile.objects.create()

    # Add children objects
    ChildKlasses = models.get_profile_child_models()
    for ChildKlass in ChildKlasses:
        ChildKlass.objects.create(profile=profile)

    if request.user:
        profile.user = request.user
        profile.fullname.text = request.user.fullname
        profile.email.text = request.user.email
        profile.save()
        profile.fullname.save()
        profile.email.save()

    return profile


def collect_profile_context(profile) -> dict:
    """
    We collect a dict with the child models as keys and its model forms as values.
    modelsforms -> ChildModels:ChildModelForms

    In order to get the context we need to get the profile child field as a string.
    We access to this string value by doing: Model._meta.model_name

    We also need to initiate the model forms with their model instances by using this code:
    Form(instance=getattr(profile, Model._meta.model_name)

    We use dict comprehension to collect all the childs

    {key:value for key, value in dict_instance.items()}
    """
    modelforms = forms.get_profile_child_modelforms()

    context = {
        Model._meta.model_name: Form(instance=getattr(profile, Model._meta.model_name))
        for Model, Form in modelforms.items()
    }
    return context
