from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404


from .forms import SettingForm
from .forms import get_profile_child_modelforms
from .models import Profile
from .models import ProfileSetting
from .models import get_profile_child_models

from apps.core.sessions import get_or_create_session


@transaction.atomic
def create_initial_profile(request) -> Profile:
    # create an empty profile
    profile = Profile.objects.create()

    # Add children objects
    ChildKlasses = get_profile_child_models()
    for ChildKlass in ChildKlasses:
        ChildKlass.objects.create(profile=profile)

    # Add setting class
    ProfileSetting.objects.create(profile=profile)

    if request.user.is_authenticated:
        profile.user = request.user
        profile.fullname.text = request.user.fullname
        profile.email.text = request.user.email
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

    {key:value for key, value in dict_instance.items()}
    """
    childforms = get_profile_child_modelforms()
    childs = {
        Model._meta.model_name: Form(instance=getattr(profile, Model._meta.model_name))
        for Model, Form in childforms.items()
    }

    return childs | {
        "profile": profile,
        "setting": SettingForm(instance=profile.setting),
    }
