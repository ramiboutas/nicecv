from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError

from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from django_htmx.http import trigger_client_event

from .models import Profile, Website, Skill, Language, Education
from .models import get_child_object, get_above_child_object, get_below_child_object
from .models import update_child_object, create_empty_child_object
from .models import set_activation_state

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
def create_object_view(request):
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
def delete_object_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.delete()
    return HttpResponse(status=200)


# htmx - profile - upload full photo
@login_required
@require_POST
def upload_full_photo_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    photo_full = request.FILES.get("photo")
    object.photo_full.save(photo_full.name, photo_full)
    context = {'object': object}
    response = HttpResponse(status=200)
    trigger_client_event(response, "fullPhotoUploadedEvent", { },)
    return response


# htmx - profile - get photo modal
@login_required
def get_photo_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {'object': object}
    return render(request, 'profiles/partials/photo/modal.html', context)


# htmx - profile - remove photo modal
@login_required
def remove_photo_modal_view(request, pk):
    return HttpResponse(status=200)


# htmx - profile - crop photo
@login_required
@require_POST
def crop_photo_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    x = int(request.POST.get("cropX"))
    y = int(request.POST.get("cropY"))
    width = int(request.POST.get("cropWidth"))
    height = int(request.POST.get("cropHeigth"))
    object = object.crop_and_save_photo(x, y, width, height)
    context = {'object': object}
    response = render(request, 'profiles/partials/photo/cropped.html', context)
    trigger_client_event(response, "photoCroppedEvent", { },)
    return response


# htmx - profile - delete photos
@login_required
@require_POST
def delete_photos_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    delete_path_file(object.photo_full.path)
    delete_path_file(object.photo.path)
    object.photo_full.delete()
    object.photo.delete()
    return HttpResponse(status=200)


# htmx - profile - save general & contact info
@login_required
@require_POST
def save_personal_information_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.first_name = request.POST.get("first_name")
    object.last_name = request.POST.get("last_name")
    object.jobtitle = request.POST.get("jobtitle")
    object.location = request.POST.get("location")
    object.date_of_birth = request.POST.get("date_of_birth")
    object.phone = request.POST.get("phone")
    object.email = request.POST.get("email")
    object.website = request.POST.get("website")
    object.save()
    return HttpResponse(status=200)


# htmx - profile - update description
@login_required
@require_POST
def update_description_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    description = request.POST.get("description")
    object.description = description
    object.save()
    return HttpResponse(status=200)


# htmx - profile - get profile settings view
@login_required
def get_profile_settings_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {'object': object}
    return render(request, 'profiles/partials/profile_settings_modal.html')


# htmx - profile - remove profile settings view
@login_required
def remove_profile_settings_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {'object': object}
    return HttpResponse(status=200)


# htmx - create child object
@login_required
@require_POST
def create_child_object_view(request, child_label, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = create_empty_child_object(child_label=child_label, profile=object)
    update_child_object(child_label=child_label, child_object=child_object, request=request)
    context = {'object': object}
    try:
        return render(request, f'profiles/partials/{child_label}/main.html', context)
    except:
        return HttpResponseServerError()


# htmx - update child object
@login_required
@require_POST
def update_child_object_view(request, child_label, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(child_label=child_label, pk=pk, profile=object)
    update_child_object(child_label=child_label, child_object=child_object, request=request)
    return HttpResponse(status=200)


# htmx - delete child object
@login_required
@require_POST
def delete_child_object_view(request, child_label, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(child_label=child_label, pk=pk, profile=object)
    child_object.delete()
    context = {'object': object}
    try:
        return render(request, f'profiles/partials/{child_label}/main.html', context)
    except:
        return HttpResponseServerError()


# htmx - insert child new form
@login_required
def insert_child_new_form_view(request, child_label, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    context = {'object': object}
    try:
        return render(request, f'profiles/partials/{child_label}/new_form.html', context)
    except:
        return HttpResponseServerError()


# htmx - remove child new form
@login_required
def remove_child_new_form_view(request, child_label, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    context = {'object': object}
    try:
        return render(request, f'profiles/partials/{child_label}/new_button.html', context)
    except:
        return HttpResponseServerError()


# htmx - copy child object
@login_required
def copy_child_object_view(request, child_label, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(child_label=child_label, pk=pk, profile=object)
    try:
        context = {'object': object, child_label: child_object}
        return render(request, f'profiles/partials/{child_label}/new_form.html', context)
    except:
        return HttpResponseServerError()


# htmx - move up child object
@login_required
def move_up_child_object_view(request, child_label, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(child_label=child_label, pk=pk, profile=object)
    above_child_object = get_above_child_object(child_label=child_label, child_object=child_object, profile=object)
    above_order = above_child_object.order
    above_child_object.order = child_object.order
    child_object.order = above_order
    above_child_object.save()
    child_object.save()
    context = {'object': object}
    try:
        return render(request, f'profiles/partials/{child_label}/main.html', context)
    except:
        return HttpResponseServerError()


# htmx - move down child object
@login_required
def move_down_child_object_view(request, child_label, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(child_label=child_label, pk=pk, profile=object)
    below_child_object = get_below_child_object(child_label=child_label, child_object=child_object, profile=object)
    below_order = below_child_object.order
    below_child_object.order = child_object.order
    child_object.order = below_order
    below_child_object.save()
    child_object.save()
    context = {'object': object}
    try:
        return render(request, f'profiles/partials/{child_label}/main.html', context)
    except:
        return HttpResponseServerError()


# htmx - activate child or profile field
@login_required
def activate_child_or_field_view(request, label, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    set_activation_state(label=label, object=object, active=True)
    context = {'object': object}
    try:
        response = render(request, f'profiles/partials/{label}/main.html', context)
        trigger_client_event(response, f'{label}ActivatedEvent', { },)
        print(f'{label}ActivatedEvent')
        return response
    except:
        return HttpResponseServerError()


# htmx - deactivate child or profile field
@login_required
def deactivate_child_or_field_view(request, label, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    set_activation_state(label=label, object=object, active=False)
    response = HttpResponse(status=200)
    trigger_client_event(response, f'{label}DeactivatedEvent', { },)
    return response


# htmx - insert activation button
@login_required
def insert_child_activation_button_view(request, label, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    context = {'object': object}
    try:
        return render(request, f'profiles/partials/{label}/activation_button.html', context)
    except:
        return HttpResponseServerError()


# htmx - remove the activation button
@login_required
def remove_child_activation_button_view(request, label, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    return HttpResponse(status=200)
