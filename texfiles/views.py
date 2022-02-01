from django_htmx.http import trigger_client_event
from django_tex.shortcuts import render_to_pdf

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import FileResponse
from django.conf import settings

from profiles.models import Profile
from .models import ResumeTemplate
from utils.files import get_tex_template_name

@login_required
@require_POST
def download_resume_view(request, pk):
    pk_profile = request.POST.get("pk_profile")
    profile_object = get_object_or_404(Profile, pk=pk_profile, user=request.user)
    resume_object = get_object_or_404(ResumeTemplate, pk=pk)
    resume_object.add_one_download()
    settings.LATEX_INTERPRETER = resume_object.interpreter
    template_name = get_tex_template_name(resume_object)
    context = {'object': profile_object}
    return render_to_pdf(request, template_name, context, filename='your_cv.pdf')

@login_required
def download_coverletter_view(request, pk):
    pass
