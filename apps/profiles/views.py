import copy

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django_htmx.http import trigger_client_event

from .forms import CropPhotoForm
from .forms import PersonalInfoForm
from .forms import ActivationForm
from .forms import LabellingForm
from .forms import create_inlineformset
from .forms import get_model_and_form
from .forms import UploadPhotoForm
from .models import Profile
from apps.accounts.models import CustomUser
from apps.core.http import HTTPResponseHXRedirect
from apps.core.objects import get_child_models
from apps.core.sessions import get_or_create_session


@transaction.atomic
def _create_initial_profile(request):
    # create an empty profile
    profile = Profile.objects.create()

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


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.filter(user=request.user)
    else:
        session, request = get_or_create_session(request)
        profiles = Profile.objects.filter(session=session)

    context = {"object_list": profiles}
    return render(request, "profiles/profile_list.html", context)


def profile_create(request):
    profile, request = _create_initial_profile(request)
    return HTTPResponseHXRedirect(redirect_to=profile.update_url())


def profile_update(request, id):
    try:
        if request.user.is_authenticated:
            profile = Profile.objects.get(id=id, user=request.user), request
        else:
            session, request = get_or_create_session(request)
            profile = Profile.objects.get(id=id, session=session)
    except Profile.DoesNotExist:
        raise Http404

    context = profile.collect_context()
    return render(request, "profiles/profile_update.html", context)


def _process_setting_form(request, form, profile):
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(profile.update_url(params={"showSettings": "true"}))
    messages.warning(request, _("Error with profile settings"))
    context = profile.collect_context()
    context["showSettings"] = True
    return render(request, "profiles/profile_update.html", context)


@require_POST
def update_labelling(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = LabellingForm(request.POST, instance=profile)
    return _process_setting_form(request, form, profile)


@require_POST
def update_activation(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = ActivationForm(request.POST, instance=profile)
    return _process_setting_form(request, form, profile)


@require_POST
def update_profile_field(request, id):
    profile = get_object_or_404(Profile, id=id)
    for key in request.POST:
        setattr(profile, key, request.POST[key])
        profile.save()
    return HttpResponse(status=200)


@require_POST
def update_personal_info(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = PersonalInfoForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
    context = {"personal_info_form": form}
    return render(request, "profiles/partials/personal_info.html", context)


def _render_child_formset(request, Model, Form, profile):
    new_formset = create_inlineformset(Form)(instance=profile)
    context = {
        "formset": new_formset,
        "update_url": profile.update_formset_url(Model),
        "order_url": profile.order_formset_url(Model),
    }
    return render(request, "profiles/partials/childset.html", context)


@require_POST
def update_child_formset(request, klass, id):
    Model, Form = get_model_and_form(klass)
    FormSet = create_inlineformset(Form)

    profile = Profile.objects.get(id=id)
    formset = FormSet(request.POST, instance=profile)
    if formset.is_valid():
        formset.save()
        return _render_child_formset(request, Model, Form, profile)

    context = {
        "message": _("Error during save process"),
        "icon": "⚠️",
        "description": mark_safe(formset.errors),
        "disappearing_time": 5000,
    }
    return render(request, "components/hx_notification.html", context)


@require_POST
def order_child_formset(request, klass, id):
    Model, Form = get_model_and_form(klass)
    FormSet = create_inlineformset(Form)
    profile = Profile.objects.get(id=id)
    formset = FormSet(request.POST, instance=profile)
    if formset.is_valid():
        ids = [int(i) for i in request.POST.getlist("child-id")]
        for order, id in enumerate(ids, start=1):
            obj = formset.queryset.get(id=id)
            obj.order = order
            obj.save()
    return _render_child_formset(request, Model, Form, profile)


@require_http_methods(["DELETE"])
def delete_child(request, klass, id):
    Model, Form = get_model_and_form(klass)
    object = get_object_or_404(Model, id=id)
    object.delete()
    return _render_child_formset(request, Model, Form, object.profile)


@require_POST
def delete_profile(request, id):
    object = get_object_or_404(Profile, id=id)
    object.delete()
    return HttpResponse(status=200)


@require_POST
def upload_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = UploadPhotoForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        saved_profile = form.save(commit=False)
        saved_profile.process_photo()

    context = {
        "cropphoto_form": CropPhotoForm(instance=saved_profile),
        "profile": profile,
    }
    return render(request, "profiles/photo/crop_form.html", context)


@require_POST
def crop_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = CropPhotoForm(request.POST, instance=profile)
    if form.is_valid():
        saved_obj = form.save(commit=False)
        saved_obj.crop_photo()
    context = {"profile": profile}
    return render(request, "profiles/photo/cropped.html", context)


@require_http_methods(["DELETE"])
def delete_photo_files(request, id):
    profile = get_object_or_404(Profile, id=id)
    profile.full_photo.delete()
    profile.cropped_photo.delete()
    profile.crop_x, profile.crop_y = None, None
    profile.crop_height, profile.crop_width = None, None

    saved_profile = profile.save()
    context = {
        "uploadphoto_form": UploadPhotoForm(instance=saved_profile),
        "profile": saved_profile,
    }
    return render(request, "profiles/photo/new.html", context)
