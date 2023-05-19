import copy

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser

from django_htmx.http import trigger_client_event

from .models import Profile
from .models import AbstractProfileChild
from .models import AbstractProfileSetting
from .forms import get_model_and_form
from .forms import get_inlineformset

from apps.core.http import HTTPResponseHXRedirect
from apps.core.sessions import get_or_create_session
from apps.accounts.models import CustomUser
from apps.core.sessions import get_or_create_session
from apps.core.objects import get_child_models


@transaction.atomic
def _create_initial_profile(request):
    # create an empty profile
    profile = Profile.objects.create()

    # Add single item children objects
    for Klass in get_child_models("profiles", AbstractProfileChild):
        Klass.objects.create(profile=profile)

    # Add setting objects
    for Klass in get_child_models("profiles", AbstractProfileSetting):
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


@require_POST
def update_settings(request, klass, id):
    Model, Form = get_model_and_form(klass)
    obj = get_object_or_404(Model, id=id)
    form = Form(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(
            obj.profile.update_url(params={"settingsopen": "true"})
        )
    messages.warning(request, _("Error with profile settings"))
    context = obj.profile.collect_context()
    context[Model._meta.model_name] = form
    context["settingsopen"] = True
    return render(request, "profiles/profile_update.html", context)


@require_POST
def update_child_form(request, klass, id):
    Model, Form = get_model_and_form(klass)
    obj = get_object_or_404(Model, id=id)
    form = Form(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        context = {"message": _("Saved"), "icon": "✅"}
    else:
        context = {
            "message": _("Error during save process"),
            "icon": "⚠️",
            "description": mark_safe(form.errors.as_ul()),
            "disappearing_time": 5000,
        }
    return render(request, "components/hx_notification.html", context)


def update_child_formset(request, klass, id):
    Model, Form = get_model_and_form(klass)
    FormSet = get_inlineformset(Form)

    profile = Profile.objects.get(id=id)
    formset = FormSet(request.POST, instance=profile)
    if formset.is_valid():
        formset.save()
        new_formset = get_inlineformset(Form)(instance=profile)
        context = {
            "update_url": profile.update_formset_url(Model),
            "order_url": profile.order_formset_url(Model),
            "formset": new_formset,
        }
        return render(request, "profiles/partials/childset.html", context)
    else:
        context = {
            "message": _("Error during save process"),
            "icon": "⚠️",
            "description": mark_safe(formset.errors),
            "disappearing_time": 5000,
        }
    return render(request, "components/hx_notification.html", context)


def order_child_formset(request, klass, id):
    Model, Form = get_model_and_form(klass)
    FormSet = get_inlineformset(Form)
    profile = Profile.objects.get(id=id)
    formset = FormSet(request.POST, instance=profile)
    if formset.is_valid():
        ids = [int(i) for i in request.POST.getlist("child-id")]
        for index, id in enumerate(ids):
            obj = formset.queryset.get(id=id)
            obj.order = index + 1
            obj.save()

    new_formset = get_inlineformset(Form)(instance=profile)
    context = {
        "update_url": profile.update_formset_url(Model),
        "order_url": profile.order_formset_url(Model),
        "formset": new_formset,
    }
    return render(request, "profiles/partials/childset.html", context)


@require_http_methods(["DELETE"])
def delete_child(request, klass, id):
    Model, Form = get_model_and_form(klass)
    object = get_object_or_404(Model, id=id)
    object.delete()
    new_formset = get_inlineformset(Form)(instance=object.profile)
    context = {
        "update_url": object.profile.update_formset_url(Model),
        "order_url": object.profile.order_formset_url(Model),
        "formset": new_formset,
    }

    return render(request, "profiles/partials/childset.html", context)


# htmx - profile - delete object
@require_POST
def delete_profile(request, id):
    object = get_object_or_404(Profile, id=id)
    object.delete()
    return HttpResponse(status=200)


# htmx - profile - upload full photo
@login_required
@require_POST
def upload_full_photo_view(request, id):
    object = get_object_or_404(Profile, id=id, user=request.user)
    photo_full = request.FILES.get("photo")
    object.photo_full.save(photo_full.name, photo_full)
    context = {"object": object}
    response = HttpResponse(status=200)
    trigger_client_event(
        response,
        "fullPhotoUploadedEvent",
        {},
    )
    return response


# htmx - profile - get photo modal
@login_required
def get_photo_modal_view(request, id):
    object = get_object_or_404(Profile, id=id, user=request.user)
    context = {"object": object}
    return render(request, "profiles/partials/photo/modal.html", context)


# htmx - profile - remove photo modal
@login_required
def remove_photo_modal_view(request, id):
    object = get_object_or_404(Profile, id=id, user=request.user)
    return HttpResponse(status=200)


# htmx - profile - crop photo
@login_required
@require_POST
def crop_photo_view(request, id):
    object = get_object_or_404(Profile, id=id, user=request.user)
    crop_x = int(request.POST.get("cropX"))
    crop_y = int(request.POST.get("cropY"))
    crop_width = int(request.POST.get("cropWidth"))
    crop_height = int(request.POST.get("cropHeigth"))
    object = object.photo.crop_photo(crop_x, crop_y, crop_width, crop_height)
    context = {"object": object}
    response = render(request, "profiles/partials/photo/cropped.html", context)
    trigger_client_event(
        response,
        "photoCroppedEvent",
        {},
    )
    return response


# htmx - profile - delete photos
@login_required
@require_POST
def delete_photos_view(request, id):
    object = get_object_or_404(Profile, id=id, user=request.user)
    object.photo_full.delete()
    object.photo.delete()
    return HttpResponse(status=200)
