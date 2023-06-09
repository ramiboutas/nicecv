from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django_htmx.http import trigger_client_event
from django_tex.shortcuts import render_to_pdf

from .models import CvTex
from apps.profiles.models import Profile


@login_required
@require_POST
def download_resume_view(request, pk):
    pk_profile = request.POST.get("pk_profile")
    profile_object = get_object_or_404(Profile, pk=pk_profile, user=request.user)
    resume = get_object_or_404(CvTex, pk=pk)
    resume.add_download()
    settings.LATEX_INTERPRETER = resume.interpreter
    context = {"object": profile_object}
    return render_to_pdf(request, resume.template_name, context, filename="your_cv.pdf")
