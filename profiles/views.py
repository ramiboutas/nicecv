from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from django_htmx.http import trigger_client_event

from .models import Profile
from utils.files import delete_path_file
User = get_user_model()

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect']=self['Location']
    status_code = 200


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/profile_update.html'
    model = Profile
    fields = '__all__'
    # exclude = ['candidate_name','candidate_position','candidate_email', 'candidate_phone','candidate_location', 'candidate_website']
    def get_object(self):
        obj = get_object_or_404(Profile, pk=self.kwargs['pk'], user=self.request.user)
        return obj

class ProfileCreateView(LoginRequiredMixin, CreateView):
    template_name = 'profiles/profile_update.html'
    model = Profile
    fields = '__all__'
    def form_valid(self, form):
        response = super(ProfileCreateView, self).form_valid(form)
        trigger_client_event(response, 'ObjectCreatedEvent', { },)
        return response


# htmx - profile - create object
@login_required
@require_POST
def hx_create_object_view(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    object = Profile(user=request.user, first_name=first_name, last_name=last_name, email=email)
    object.save()
    # once the object is created, we redirect the user to the obj update url
    return HTTPResponseHXRedirect(redirect_to=object.get_update_url())


# htmx - profile - delete object
@login_required
@require_POST
def hx_delete_object_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.delete()
    return HttpResponse(status=200)


# htmx - profile - upload full photo
@login_required
@require_POST
def hx_upload_full_photo_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    photo_full = request.FILES.get("photo")
    object.photo_full.save(photo_full.name, photo_full)
    context = {'object': object}
    response = HttpResponse(status=200)
    trigger_client_event(response, "fullPhotoUploadedEvent", { },)
    return response


# htmx - profile - get photo modal
@login_required
def hx_get_photo_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {'object': object}
    return render(request, 'profiles/partials/photo_modal.html', context)


# htmx - profile - remove photo modal
@login_required
def hx_remove_photo_modal_view(request, pk):
    return HttpResponse(status=200)


# htmx - profile - crop photo
@login_required
@require_POST
def hx_crop_photo_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    x = int(request.POST.get("cropX"))
    y = int(request.POST.get("cropY"))
    width = int(request.POST.get("cropWidth"))
    height = int(request.POST.get("cropHeigth"))
    object = object.crop_and_save_photo(x, y, width, height)
    context = {'object': object}
    response = render(request, 'profiles/partials/photo_cropped.html', context)
    trigger_client_event(response, "photoCroppedEvent", { },)
    return response

# htmx - profile - delete photos
@login_required
@require_POST
def hx_delete_photos_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    delete_path_file(object.photo_full.path)
    delete_path_file(object.photo.path)
    object.photo_full.delete()
    object.photo.delete()
    return HttpResponse(status=200)


@login_required
@require_POST
def hx_save_general_and_contact_info_view(request, pk):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
