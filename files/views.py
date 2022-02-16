from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _

from celery.result import AsyncResult
from celery_progress_htmx.backend import Progress

from .models import ResumeFile
from .tasks import create_resume_file_objects
from profiles.models import Profile

@never_cache
def generate_resumes_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    result =  create_resume_file_objects.delay(pk=pk)
    profile.task_id = result.task_id
    profile.save()
    context = {'object': profile}
    return render(request, 'files/partials/resume_creation_status.html', context)




@never_cache
def resume_creation_status_view(request, pk, task_id):
    profile = get_object_or_404(Profile, pk=pk)
    progress_object = Progress(AsyncResult(profile.task_id))
    progress = progress_object.get_info().get("progress")
    percent = progress.get("percent")
    success = progress_object.get_info().get("success")
    context = { 'percent': percent,'object': profile}
    if percent == 100 and success:
        return render(request, 'files/partials/resume_creation_success.html', context)
    if success == False:
        messages.error(request, _('Unespected error'))
        return render(request, 'files/partials/resume_creation_error.html', context)
    return render(request, 'files/partials/resume_creation_status.html', context)


def resume_file_list_view(request, pk):
    qs = ResumeFile.objects.filter(profile__user=request.user, profile__pk=pk)
    context = {'object_list': qs}
    return render(request, 'files/resumefile_list.html', context)
