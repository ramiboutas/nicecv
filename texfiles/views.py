from django_htmx.http import trigger_client_event
from django_tex.shortcuts import render_to_pdf

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import FileResponse

from profiles.models import Profile
from .models import ResumeTemplate
from utils.files import get_tex_template_name

@login_required
def download_resume_view(request, pk):

    pk_profile = request.POST.get("pk_profile") # introduce the pk_profile in a hidden input

    profile_object = get_object_or_404(Profile, pk=pk_profile, user=request.user)

    resume_object = get_object_or_404(ResumeTemplate, pk=pk)
    context = {'object': profile_object}
    template_name = get_tex_template_name(resume_object)
    return render_to_pdf(request, template_name, context, filename='your_cv.pdf')

    # if request.method == 'POST':
    #     result = process_download.delay(request.POST, pk)
    #     # update number of downloads in the tex file
    #     texfile_obj = TexFile.objects.get(pk=int(request.POST.get("texfileselected_pk")))
    #     texfile_obj.downloads = texfile_obj.downloads + 1
    #     texfile_obj.save()
    #     context={'task_id': result.task_id, 'object': object}
    #     return render(request, 'processing_download.html', context)
    # return redirect(object.get_update_url()) # we had to add this because if user selects language change in the downloading page, we need to redirect him to somewhere

@login_required
def download_coverletter_view(request, pk):
    pass
