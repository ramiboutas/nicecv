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

from .models import Profile, Website, Skill, Language, Education
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
    return render(request, 'profiles/partials/photo_modal.html', context)


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
    response = render(request, 'profiles/partials/photo_cropped.html', context)
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
def save_general_and_contact_info_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.first_name = request.POST.get("first_name")
    object.last_name = request.POST.get("last_name")
    object.jobtitle = request.POST.get("jobtitle")
    object.location = request.POST.get("location")
    object.date_of_birth = request.POST.get("date_of_birth")
    object.phone = request.POST.get("phone")
    object.email = request.POST.get("email")
    object.save()
    return HttpResponse(status=200)


def get_website_boostrap_icon(text):
    icon_list = ['github', 'facebook', 'instagram', 'linkedin', 'medium', 'quora', 'reddit', 'skype', 'slack', 'stack-overflow', 'telegram', 'twitch', 'twitter', 'vimeo', 'youtube']

    # use list comprehension!!!
    for index, icon in enumerate(icon_list):
        if icon.replace("-", "") in text:
            return icon_list[index]
    return 'globe'

# htmx - profile - add website object
@login_required
@require_POST
def add_website_object_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    name = request.POST.get("website_name_new")
    bootstrap_icon = get_website_boostrap_icon(str(name))
    website_object = Website(name=name, profile=object, bootstrap_icon=bootstrap_icon)
    website_object.save()
    context = {'object': object}
    return render(request, 'profiles/partials/websites.html', context)


# htmx - profile - update website object
@login_required
@require_POST
def update_website_object_view(request, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    website_object = get_object_or_404(Website, pk=pk, profile=object)
    name = request.POST.get("website_name")
    website_object.name = name
    website_object.save()
    return HttpResponse(status=200)

# htmx - profile - delete website object
@login_required
@require_POST
def delete_website_object_view(request, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    website_object = get_object_or_404(Website, pk=pk, profile=object)
    website_object.delete()
    return HttpResponse(status=200)


# htmx - profile - add skill object
@login_required
@require_POST
def add_skill_object_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    name = request.POST.get("skill_name_new")
    skill_object = Skill(name=name, profile=object)
    skill_object.save()
    context = {'object': object}
    return render(request, 'profiles/partials/skills.html', context)


# htmx - profile - update skill object
@login_required
@require_POST
def update_skill_object_view(request, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    skill_object = get_object_or_404(Skill, pk=pk, profile=object)
    name = request.POST.get("skill_name")
    skill_object.name = name
    skill_object.save()
    return HttpResponse(status=200)

# htmx - profile - delete skill object
@login_required
@require_POST
def delete_skill_object_view(request, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    skill_object = get_object_or_404(Skill, pk=pk, profile=object)
    skill_object.delete()
    return HttpResponse(status=200)


# htmx - profile - add language object
@login_required
@require_POST
def add_language_object_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    name = request.POST.get("language_name_new")
    level = request.POST.get("language_level_new")
    language_object = Language(name=name, level=level, profile=object)
    language_object.save()
    context = {'object': object}
    return render(request, 'profiles/partials/languages.html', context)


# htmx - profile - update language object
@login_required
@require_POST
def update_language_object_view(request, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    language_object = get_object_or_404(Language, pk=pk, profile=object)
    name = request.POST.get("language_name")
    level = request.POST.get("language_level")
    language_object.name = name
    language_object.level = level
    language_object.save()
    return HttpResponse(status=200)

# htmx - profile - delete language object
@login_required
@require_POST
def delete_language_object_view(request, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    language_object = get_object_or_404(Language, pk=pk, profile=object)
    language_object.delete()
    return HttpResponse(status=200)




# htmx - profile - add description
@login_required
@require_POST
def activate_description_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.description_active = True
    object.save()
    context = {'object': object}
    response = render(request, 'profiles/partials/description.html', context)
    trigger_client_event(response, "descriptionActivatedEvent", { },)
    return response


# htmx - profile - deactivate description
@login_required
@require_POST
def deactivate_description_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    object.description_active = False
    object.save()
    response = HttpResponse(status=200)
    trigger_client_event(response, "descriptionDeactivatedEvent", { },)
    return response



# htmx - profile - update description
@login_required
@require_POST
def update_description_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    description = request.POST.get("description")
    object.description = description
    object.save()
    return HttpResponse(status=200)



# htmx - profile - add "add description button"
@login_required
def insert_description_button_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {'object': object}
    return render(request, 'profiles/partials/description_activate_button.html', context)


# htmx - profile - delete "add description button"
@login_required
def remove_description_button_view(request, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    return HttpResponse(status=200)


# htmx - profile - add education object
@login_required
@require_POST
def create_child_object_view(request, obj, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)

    # create_child_object(child_label=obj, post_dict=request.POST, profile=object) # include this function in models.py

    title = request.POST.get("education_title_new")
    subtitle = request.POST.get("education_subtitle_new")
    grade = request.POST.get("education_grade_new")
    start_date = request.POST.get("education_start_date_new")
    end_date = request.POST.get("education_end_date_new")
    institution = request.POST.get("education_institution_new")
    description = request.POST.get("education_description_new")
    education_object = Education(profile=object, title=title, subtitle=subtitle, grade=grade, start_date=start_date, end_date=end_date, institution=institution, description=description)
    education_object.save()

    context = {'object': object}
    return render(request, 'profiles/partials/education.html', context)


# htmx - profile - update education object
@login_required
@require_POST
def update_child_object_view(request, obj, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    education_object = get_object_or_404(Education, pk=pk, profile=object)
    education_object.start_date = request.POST.get("education_start_date")
    education_object.end_date = request.POST.get("education_end_date")
    education_object.grade = request.POST.get("education_grade")
    education_object.title = request.POST.get("education_title")
    education_object.subtitle = request.POST.get("education_subtitle")
    education_object.institution = request.POST.get("education_institution_new")
    education_object.description = request.POST.get("education_description")
    education_object.save()
    return HttpResponse(status=200)

# htmx - profile - delete education object
@login_required
@require_POST
def delete_child_object_view(request, obj, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    education_object = get_object_or_404(Education, pk=pk, profile=object)
    education_object.delete()
    return HttpResponse(status=200)

@login_required
def insert_child_new_form_view(request, obj, pk):
    print(obj)
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {'object': object}
    return render(request, 'profiles/partials/education_new_form.html', context)

@login_required
def remove_child_new_form_view(request, obj, pk):
    object = get_object_or_404(Profile, pk=pk, user=request.user)
    context = {'object': object}
    return render(request, 'profiles/partials/education_new_button.html', context)


@login_required
def remove_child_new_form_view(request, obj, pk_parent, pk):
    pass


@login_required
def copy_child_object_view(request, obj, pk_parent, pk):
    pass


@login_required
def move_up_child_object_view(request, obj, pk_parent, pk):
    object = get_object_or_404(Profile, pk=pk_parent, user=request.user)
    child_object = get_object_or_404(Education, profile=object, pk=pk)
    above_order = child_object.order-1
    object_order = child_object.order
    above_child_object = Education.objects.get(order=above_order, profile=object)
    above_child_object.order = object_order
    child_object.order = above_order
    above_child_object.save()
    child_object.save()
    return  HttpResponse("ordered")





@login_required
def move_down_child_object_view(request, obj, pk_parent, pk):
    pass


@login_required
def activate_child_object_view(request, obj, pk):
    pass


@login_required
def deactivate_child_object_view(request, obj, pk):
    pass
