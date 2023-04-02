import inspect
from functools import cache

from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404


from .models import Profile
from .models import ProfileOneChild
from .models import ProfileSettings

from .forms import SingleItemChildForm
from .forms import ProfileSettingsForm

from apps.accounts.models import CustomUser
from apps.core.sessions import get_or_create_session
from apps.core.classes import get_child_models


@transaction.atomic
def create_initial_profile(request) -> Profile:
    # create an empty profile
    profile = Profile.objects.create()

    # Add single item children objects
    for Klass in get_child_models("profiles", ProfileOneChild):
        Klass.objects.create(profile=profile)

    # Add setting objects
    for Klass in get_child_models("profiles", ProfileSettings):
        Klass.objects.create(profile=profile)

    user = getattr(request, "user", AnonymousUser())
    if isinstance(user, CustomUser):
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
        field_name = Model._meta.model_name
        context[field_name] = Form(
            instance=getattr(profile, field_name), auto_id="id_%s_" + field_name
        )

    context["profile"] = profile
    from .forms import SkillFormSet
    from .forms import SkillForm

    context["skills"] = SkillFormSet(profile=profile)
    context["skill"] = SkillForm()
    return context


@cache
def get_profile_modelforms(settings=False, singles=True, many=True) -> dict:
    """Returns a dict with model classes and form classes asociated with Profile model"""
    from . import forms

    KlassDict = {}
    Forms = [k for _, k in inspect.getmembers(forms, inspect.isclass)]

    for Form in Forms:
        if singles and (SingleItemChildForm in Form.__bases__):
            KlassDict[Form.Meta.model] = Form
        if settings and (ProfileSettingsForm in Form.__bases__):
            KlassDict[Form.Meta.model] = Form

    return KlassDict


@cache
def get_modelform(Klass):
    """Returns the ModelForm associated with a Profile Model"""
    from . import models

    Model = getattr(models, Klass) if isinstance(Klass, str) else Klass
    modelforms = get_profile_modelforms(settings=True)
    return Model, modelforms[Model]
