from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.http import HttpResponseServerError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django_htmx.http import trigger_client_event

from .models import Profile
from .forms import ProfileCreationForm
from .forms import ProfileUpdateForm
from apps.core.http import HTTPResponseHXRedirect


@login_required
def profile_list_view(request):
    context = {"object_list": Profile.objects.filter(user=request.user)}
    return render(request, "profiles/profile_list.html", context)


def _get_profile_initial_data(request) -> dict:
    if request.user:
        return {
            "user": request.user,
            "fullname": request.user.first_name + " " + request.user.last_name,
            "email": request.user.email,
        }
    return {}


def profile_create_view(request):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            profile = form.save()
            return HTTPResponseHXRedirect(redirect_to=profile.update_url)
    else:
        form = ProfileCreationForm(initial=_get_profile_initial_data(request))

    return render(request, "profiles/profile_create.html", {"form": form})


def profile_update_view(request, id):
    profile = get_object_or_404(Profile, id=id, user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)
    context = {"object": profile, "profile_form": profile_form}
    return render(request, "profiles/profile_update.html", context)


@require_POST
def profile_update_fields_view(request, id):
    form = ProfileUpdateForm(request.POST)
    if form.is_valid():
        profile_form = form.save()
        context = {"profile_form": form}

        return render(request, "profiles/hs/profile_fields.html", context)


# htmx - profile - delete object
@login_required
@require_POST
def delete_object_view(request, id):
    object = get_object_or_404(Profile, id=id, user=request.user)
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
