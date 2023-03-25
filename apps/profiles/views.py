from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django_htmx.http import trigger_client_event


from .forms import get_child_modelform
from .forms import ActiveSettingForm
from .forms import LabelSettingForm
from .models import Profile
from apps.core.http import HTTPResponseHXRedirect
from apps.core.sessions import get_or_create_session

from .utils import create_initial_profile
from .utils import collect_profile_context
from .utils import get_profile_instance
from .utils import get_profile_list


def profile_list(request):
    profiles, request = get_profile_list(request)
    context = {"object_list": profiles}
    return render(request, "profiles/profile_list.html", context)


def profile_create(request):
    profile, request = create_initial_profile(request)
    return HTTPResponseHXRedirect(redirect_to=profile.update_url)


def profile_update(request, id):
    profile, request = get_profile_instance(request, id)
    context = collect_profile_context(profile)
    return render(request, "profiles/profile_update.html", context)


def profile_settings(request, id):
    profile, request = get_profile_instance(request, id)
    if request.method == "POST":
        active_form = ActiveSettingForm(request.POST, instance=profile.activesetting)
        label_form = LabelSettingForm(request.POST, instance=profile.labelsetting)
        if active_form.is_valid() and label_form.is_valid():
            active_form.save()
            label_form.save()
            HttpResponseRedirect(profile.update_url)
    else:
        active_form = ActiveSettingForm(instance=profile.activesetting)
        label_form = LabelSettingForm(instance=profile.labelsetting)
    context = {"active_form": active_form, "label_form": label_form}
    return render(request, "profiles/profile_settings.html", context)


@require_POST
def update_child(request, klass, id):
    ChildModel, ChildForm = get_child_modelform(klass)
    obj = get_object_or_404(ChildModel, id=id)
    form = ChildForm(request.POST, instance=obj)
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


# htmx - profile - delete object


@require_POST
def delete_object(request, id):
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
