import inspect
from functools import cache

from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404


from .models import Profile
from .models import ProfileChild
from .models import ProfileSettings

from .forms import ChildForm
from .forms import BaseChildFormSet
from .forms import SettingsForm

from apps.accounts.models import CustomUser
from apps.core.sessions import get_or_create_session
from apps.core.classes import get_child_models


@transaction.atomic
def create_initial_profile(request) -> Profile:
    # create an empty profile
    profile = Profile.objects.create()

    # Add single item children objects
    for Klass in get_child_models("profiles", ProfileChild):
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
    context = {}

    # Adding the profile instance itself
    context["profile"] = profile

    # gather child forms (one to one relationship to profile)
    setting_and_child_forms = get_childforms() | get_settingforms()
    for Model, Form in setting_and_child_forms.items():
        name = Model._meta.model_name
        context[name] = Form(instance=getattr(profile, name), auto_id="id_%s_" + name)

    # gather child formsets (many to one relationship to profile)
    for Model, FormSet in get_childformsets().items():
        name = Model._meta.model_name
        context[name] = FormSet(
            profile=profile,
            update_url=profile.update_formset_url(Model.__name__),
            auto_id="id_%s_" + name,
        )

    return context


@cache
def get_classes_from_forms() -> list:
    from . import forms

    return [k for _, k in inspect.getmembers(forms, inspect.isclass)]


@cache
def get_model(Klass):
    from . import models

    return getattr(models, Klass) if isinstance(Klass, str) else Klass


@cache
def get_childforms() -> dict:
    Forms = get_classes_from_forms()
    return {Form.Meta.model: Form for Form in Forms if ChildForm in Form.__bases__}


@cache
def get_settingforms() -> dict:
    Forms = get_classes_from_forms()
    return {Form.Meta.model: Form for Form in Forms if SettingsForm in Form.__bases__}


@cache
def get_childformsets() -> dict:
    Forms = get_classes_from_forms()
    return {Form.model: Form for Form in Forms if BaseChildFormSet in Form.__bases__}


@cache
def get_child_model_and_form(Klass):
    """Returns a tuple: ChildModel, ChildModelForm"""
    Model = get_model(Klass)
    modelforms = get_childforms()
    return Model, modelforms[Model]


@cache
def get_setting_model_and_form(Klass):
    """Returns a tuple: SettingModel, SettingModelForm"""
    Model = get_model(Klass)
    modelforms = get_settingforms()
    return Model, modelforms[Model]


@cache
def get_child_model_and_formset(Klass):
    """Returns a tuple: ChildSetModel, ChildSetModelForm"""
    Model = get_model(Klass)
    modelforms = get_childformsets()
    return Model, modelforms[Model]
