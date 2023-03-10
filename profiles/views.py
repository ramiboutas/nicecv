from celery.result import AsyncResult
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django_htmx.http import trigger_client_event

from .models import create_empty_child_object
from .models import get_above_child_object
from .models import get_below_child_object
from .models import get_child_object
from .models import Profile
from .models import Resume
from .models import set_activation_state
from .models import update_child_object
from .tasks import create_resume_objects
from celery_progress_htmx.backend import Progress
from utils.files import delete_file


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "profiles/profile_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]

    status_code = 200


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "profiles/profile_update.html"
    model = Profile
    fields = "__all__"
    # exclude = ['candidate_name','candidate_position','candidate_email', 'candidate_phone','candidate_location', 'candidate_website']
    def get_object(self):
        obj = get_object_or_404(Profile, pk=self.kwargs["pk"], user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["debug_flag"] = settings.DEBUG
        return context


class ProfileCreateView(LoginRequiredMixin, CreateView):
    template_name = "profiles/profile_update.html"
    model = Profile
    fields = "__all__"

    def form_valid(self, form):
        response = super().form_valid(form)
        trigger_client_event(
            response,
            "ObjectCreatedEvent",
            {},
        )
        return response


# htmx - profile - create object
@login_required
@require_POST
def create_object_view(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    email = request.POST.get("email")
    object = Profile(
        user=request.user, firstname=firstname, lastname=lastname, email=email
    )
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
def get_photo_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {"object": object}
    return render(request, "profiles/partials/photo/modal.html", context)


# htmx - profile - remove photo modal
@login_required
def remove_photo_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
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
def delete_photos_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    delete_file(object.photo_full.path)
    delete_file(object.photo.path)
    object.photo_full.delete()
    object.photo.delete()
    return HttpResponse(status=200)


# htmx - profile - get resume templates modal
@login_required
def insert_resume_templates_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {"object": object}
    return render(request, "profiles/partials/resume_templates_modal.html", context)


# htmx - profile - remove resume templates modal
@login_required
def remove_resume_templates_modal_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    return HttpResponse(status=200)


# htmx - profile - save general & contact info
@login_required
@require_POST
def save_personal_information_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.firstname = request.POST.get("firstname")
    object.lastname = request.POST.get("lastname")
    object.jobtitle = request.POST.get("jobtitle")
    object.location = request.POST.get("location")
    object.date_of_birth = request.POST.get("date_of_birth")
    object.phone = request.POST.get("phone")
    object.email = request.POST.get("email")
    object.website = request.POST.get("website")
    object.save()
    return HttpResponse(status=200)


# htmx - profile - update field
def update_field_view(request, slug, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.update_field(slug=slug, request=request)
    description = request.POST.get("description")
    object.description = description
    object.save()
    response = HttpResponse(status=200)
    trigger_client_event(
        response,
        "profileUpdatedEvent",
        {},
    )
    return response


#
#
# # htmx - profile - update description
# @login_required
# @require_POST
# def update_description_view(request, pk):
#     object = get_object_or_404(Profile, pk=pk, user=request.user)
#     description = request.POST.get("description")
#     object.description = description
#     object.save()
#     trigger_client_event(response, 'profileUpdatedEvent', { },)
#     return HttpResponse(status=200)


# htmx - create child object
@login_required
@require_POST
def create_child_object_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = create_empty_child_object(slug=slug, profile=object)
    update_child_object(slug=slug, child_object=child_object, request=request)
    context = {"object": object}
    try:
        response = render(request, f"profiles/partials/{slug}/main.html", context)
        trigger_client_event(
            response,
            "profileUpdatedEvent",
            {},
        )
        return response
    except:
        return HttpResponseServerError()


# htmx - update child object
@login_required
@require_POST
def update_child_object_view(request, slug, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(slug=slug, pk=pk, profile=object)
    update_child_object(slug=slug, child_object=child_object, request=request)
    response = HttpResponse(status=200)
    trigger_client_event(
        response,
        "profileUpdatedEvent",
        {},
    )
    return response


# htmx - delete child object
@login_required
@require_POST
def delete_child_object_view(request, slug, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(slug=slug, pk=pk, profile=object)
    child_object.delete()
    context = {"object": object}
    try:
        response = render(request, f"profiles/partials/{slug}/main.html", context)
        trigger_client_event(
            response,
            "profileUpdatedEvent",
            {},
        )
        return response
    except:
        return HttpResponseServerError()


# htmx - insert child new form
@login_required
def insert_child_new_form_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    context = {"object": object}
    try:
        return render(request, f"profiles/partials/{slug}/new_form.html", context)
    except:
        return HttpResponseServerError()


# htmx - remove child new form
@login_required
def remove_child_new_form_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    context = {"object": object}
    try:
        return render(request, f"profiles/partials/{slug}/new_button.html", context)
    except:
        return HttpResponseServerError()


# htmx - copy child object
@login_required
def copy_child_object_view(request, slug, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(slug=slug, pk=pk, profile=object)
    try:
        context = {"object": object, slug: child_object}
        return render(request, f"profiles/partials/{slug}/new_form.html", context)
    except:
        return HttpResponseServerError()


# htmx - move up child object
@login_required
def move_up_child_object_view(request, slug, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(slug=slug, pk=pk, profile=object)
    above_child_object = get_above_child_object(
        slug=slug, child_object=child_object, profile=object
    )
    above_order = above_child_object.order
    above_child_object.order = child_object.order
    child_object.order = above_order
    above_child_object.save()
    child_object.save()
    context = {"object": object}
    try:
        response = render(request, f"profiles/partials/{slug}/main.html", context)
        trigger_client_event(
            response,
            "profileUpdatedEvent",
            {},
        )
        return response
    except:
        return HttpResponseServerError()


# htmx - move down child object
@login_required
def move_down_child_object_view(request, slug, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_child_object(slug=slug, pk=pk, profile=object)
    below_child_object = get_below_child_object(
        slug=slug, child_object=child_object, profile=object
    )
    below_order = below_child_object.order
    below_child_object.order = child_object.order
    child_object.order = below_order
    below_child_object.save()
    child_object.save()
    context = {"object": object}
    try:
        response = render(request, f"profiles/partials/{slug}/main.html", context)
        trigger_client_event(
            response,
            "profileUpdatedEvent",
            {},
        )
        return response
    except:
        return HttpResponseServerError()


# htmx - activate child or profile field
@login_required
def activate_child_or_field_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    set_activation_state(slug=slug, object=object, active=True)
    context = {"object": object}
    try:
        response = render(request, f"profiles/partials/{slug}/main.html", context)
        trigger_client_event(
            response,
            f"{slug}ActivatedEvent",
            {},
        )
        return response
    except:
        return HttpResponseServerError()


# htmx - deactivate child or profile field
@login_required
def deactivate_child_or_field_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    set_activation_state(slug=slug, object=object, active=False)
    response = HttpResponse(status=200)
    trigger_client_event(
        response,
        f"{slug}DeactivatedEvent",
        {},
    )
    return response


# htmx - insert activation button
@login_required
def insert_child_activation_button_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    context = {"object": object}
    try:
        response = render(
            request, f"profiles/partials/{slug}/activation_button.html", context
        )
        trigger_client_event(
            response,
            "profileUpdatedEvent",
            {},
        )
        return response
    except:
        return HttpResponseServerError()


# htmx - remove the activation button
@login_required
def remove_child_activation_button_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    response = HttpResponse(status=200)
    trigger_client_event(
        response,
        "profileUpdatedEvent",
        {},
    )
    return response


# htmx - insert help modal
@login_required
def insert_child_or_field_help_modal_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    context = {"object": object}
    try:
        return render(request, f"profiles/partials/{slug}/help_modal.html", context)
    except:
        return HttpResponseServerError()


# htmx - remove help modal
@login_required
def remove_child_or_field_help_modal_view(request, slug, pk_parent):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    return HttpResponse(status=200)


##############################################################################
@login_required
def insert_button_to_generate_resumes_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {"object": profile}
    return render(
        request, "profiles/resume_partials/generate_resumes_button.html", context
    )


@never_cache
@login_required
def generate_resumes_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk, user=request.user)
    result = create_resume_objects.delay(pk=pk)
    profile.task_id = result.task_id
    profile.save()
    context = {"object": profile}
    return render(request, "profiles/resume_partials/resume_progress_bar.html", context)


@never_cache
@login_required
def resume_creation_status_view(request, pk, task_id):
    profile = get_object_or_404(Profile, pk=pk, user=request.user)
    progress_object = Progress(AsyncResult(profile.task_id))

    progress = progress_object.get_info().get("progress")
    percent = progress.get("percent")
    success = progress_object.get_info().get("success")

    context = {"progress": progress, "object": profile}

    if percent == 100 and success:
        messages.success(request, _("Resumes created successfully"))
        return render(
            request, "profiles/resume_partials/view_resumes_button.html", context
        )

    if success == False:
        messages.error(request, _("Unespected error, try again or later"))
        return render(
            request, "profiles/resume_partials/generate_resumes_button.html", context
        )

    return render(request, "profiles/resume_partials/resume_progress_bar.html", context)


@login_required
def resume_file_list_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    # qs = Resume.objects.filter(profile__user=request.user, profile__pk=pk)
    context = {"object": object}
    return render(request, "profiles/resume_list.html", context)


@login_required
def download_resume_pdf_view(request, pk_parent, pk):
    profile = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    resume = get_object_or_404(Resume, profile=profile, pk=pk)
    return FileResponse(open(resume.pdf.path, "rb"))


@login_required
def download_resume_image_view(request, pk_parent, pk):
    profile = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    resume = get_object_or_404(Resume, profile=profile, pk=pk)
    return FileResponse(open(resume.image.path, "rb"))


from django_tex.shortcuts import render_to_pdf
from tex.models import ResumeTemplate


def generate_resume_testing_view(request, pk):
    tex_template_id = request.POST.get("tex_template_id")
    resume_template = ResumeTemplate.objects.get(id=tex_template_id)
    profile = get_object_or_404(Profile, pk=pk)
    template_name = resume_template.template_name
    context = {"object": profile}
    return render_to_pdf(
        request,
        template_name,
        context,
        filename=f"{template_name}_test.pdf",
    )
