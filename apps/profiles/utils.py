from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404

from .forms import get_profile_modelforms
from .forms import ActivationSettingsForm
from .forms import LabelSettingsForm

from .models import Profile
from .models import SimpleChild
from .models import ActivationSettings
from .models import LabelSettings

from apps.core.sessions import get_or_create_session
from apps.core.classes import get_child_models


@transaction.atomic
def create_initial_profile(request) -> Profile:
    # create an empty profile
    profile = Profile.objects.create()

    # Add children objects
    ChildKlasses = get_child_models("profiles", SimpleChild)

    for ChildKlass in ChildKlasses:
        ChildKlass.objects.create(profile=profile)

    # Add setting objects
    ActivationSettings.objects.create(profile=profile)
    LabelSettings.objects.create(profile=profile)

    user = getattr(request.user, "is_authenticated", None)

    if user:
        profile.user = user
        profile.fullname.text = user.fullname
        profile.email.text = user.email
        profile.save()
        profile.fullname.save()
        profile.email.save()
    else:
        session, request = get_or_create_session(request)
        if Profile.objects.filter(session=session).count() >= 1:
            messages.warning(request, _("Only one profile is allowed for guest users"))
            return Profile.objects.filter(session=session).first(), request
        profile.category = "temporal"
        profile.session = session
        profile.save()
    return profile, request


def get_profile_instance(request, id):
    try:
        if request.user.is_authenticated:
            return Profile.objects.get(id=id, user=request.user), request

        session, request = get_or_create_session(request)
        return Profile.objects.get(id=id, session=session), request
    except Profile.DoesNotExist:
        raise Http404


def get_profile_list(request):
    if request.user.is_authenticated:
        return Profile.objects.filter(user=request.user), request
    session, request = get_or_create_session(request)
    return Profile.objects.filter(session=session), request


def collect_profile_context(profile) -> dict:
    """
    We collect a dict with the child models as keys and its model forms as values.
    modelsforms -> ChildModels:ChildModelForms

    In order to get the context we need to get the profile child field as a string.
    We access to this string value by doing: Model._meta.model_name

    We also need to initiate the model forms with their model instances by using this code:
    Form(instance=getattr(profile, Model._meta.model_name)

    We use dict comprehension to collect all the childs

    """
    childforms = get_profile_modelforms(settings=True)
    context = {}
    for Model, Form in childforms.items():
        field = Model._meta.model_name
        context[field] = Form(
            instance=getattr(profile, field), auto_id="id_%s_" + field
        )
        print(f"{field=}")
    context["profile"] = profile

    return context
