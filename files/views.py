from django.shortcuts import render
from django.views.generic.list import ListView

from .models import ResumeFile
from .tasks import create_resume_file_objects

def resumefile_list_view(request, pk):
    # create_resume_file_objects.delay(pk=pk)
    qs = ResumeFile.objects.filter(profile__user=request.user, profile__pk=pk)
    context = {'object_list': qs}
    return render(request, 'files/resumefile_list.html', context)
