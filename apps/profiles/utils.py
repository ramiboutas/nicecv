import inspect
from functools import cache

from django.db import transaction
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from apps import profiles
from .models import Profile
from .models import ProfileChild
from .models import ProfileSetting

from .forms import BaseChildForm
from .forms import BaseChildFormSet
from .forms import BaseSettingForm

from .forms import get_inlineformset

from apps.accounts.models import CustomUser
from apps.core.sessions import get_or_create_session
from apps.core.classes import get_child_models


@cache
def get_forms(singles=False, inlines=False, settings=False, get_all=False) -> dict:
    out = {}
    Forms = [k for _, k in inspect.getmembers(profiles.forms, inspect.isclass)]

    if singles or get_all:
        out = out | {F.Meta.model: F for F in Forms if BaseChildForm in F.__bases__}

    if settings or get_all:
        out = out | {F.Meta.model: F for F in Forms if BaseSettingForm in F.__bases__}

    if inlines or get_all:
        out = out | {F.Meta.model: F for F in Forms if BaseChildFormSet in F.__bases__}

    return out


@cache
def get_model_and_form(Klass):
    """Returns a tuple: ChildModel, ChildModelForm"""
    Model = getattr(profiles.models, Klass) if isinstance(Klass, str) else Klass
    modelforms = get_forms(get_all=True)
    return Model, modelforms[Model]


@transaction.atomic
def create_initial_profile(request) -> Profile:
    # create an empty profile
    profile = Profile.objects.create()

    # Add single item children objects
    for Klass in get_child_models("profiles", ProfileChild):
        Klass.objects.create(profile=profile)

    # Add setting objects
    for Klass in get_child_models("profiles", ProfileSetting):
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
    for Model, Form in get_forms(singles=True, settings=True).items():
        model_name = Model._meta.model_name

        context[model_name] = Form(
            instance=getattr(profile, model_name), auto_id="id_%s_" + model_name
        )

    # gather child formsets (many to one relationship to profile)
    # for Model, FormSet in get_forms(inlines=True).items():
    #     InlineFormSet = get_inlineformset(Model, FormSet)
    #     context[Model._meta.model_name] = InlineFormSet(
    #         instance=profile, queryset=Model.objects.filter(profile=profile)
    #     )
    for Model, Form in get_forms(inlines=True).items():
        context[Model._meta.model_name] = get_inlineformset(Form)(instance=profile)

    return context
