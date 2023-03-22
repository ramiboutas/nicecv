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
from .models import Fullname
from .models import get_class_object
from .forms import ProfileCreationForm
from .forms import ProfileForm
from .forms import FullnameTextForm
from .forms import get_form_object
from apps.core.http import HTTPResponseHXRedirect


@login_required
def profile_list(request):
    context = {"object_list": Profile.objects.filter(user=request.user)}
    return render(request, "profiles/profile_list.html", context)


def _get_initial_profile_instance(request) -> Profile:
    # TODO: move to models.py

    if request.user:
        fullname = request.user.first_name + " " + request.user.last_name
        # TODO: "email": request.user.email,
        profile = Profile.objects.create(user=request.user)
    else:
        fullname = ""
        profile = Profile.objects.create()

    # Add children objects
    Fullname.objects.create(text=fullname, profile=profile)
    return profile


def profile_create(request):
    profile = _get_initial_profile_instance(request)
    return HTTPResponseHXRedirect(redirect_to=profile.update_url)


def profile_update(request, id):
    profile = get_object_or_404(Profile, id=id, user=request.user)
    profile_form = ProfileForm(instance=profile)
    fullname_form = FullnameTextForm(instance=profile.fullname)
    context = {
        "object": profile,
        "profile_form": profile_form,
        "fullname_form": fullname_form,
    }
    return render(request, "profiles/profile_update.html", context)


def update_child_form(request, klass, form, id):
    Child = get_class_object(klass)
    ChildForm = get_form_object(form)
    obj = get_object_or_404(Child, id=id)
    form = ChildForm(request.POST, instance=obj)
    if form.is_valid():
        child_name = Child._meta.verbose_name.title()
        context = {
            "message": _(f"{child_name} saved"),
            "icon": "✅",
        }
        return render(request, "components/hx_notification.html", context)


@require_POST
def profile_update_fields(request, id):
    profile = get_object_or_404(Profile, id=id, user=request.user)
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        context = {"message": _("Profile saved"), "icon": "✅"}
        return render(request, "components/hx_notification.html", context)


# htmx - profile - delete object
@login_required
@require_POST
def delete_object(request, id):
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
