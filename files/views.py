from django.shortcuts import render
from django.views.generic.list import ListView

from .models import ResumeFile
from .tasks import create_resume_file_objects

def start_creating_resume_files_view(request, pk):
    result =  create_resume_file_objects.delay(pk=pk)
    context = {'task_id': result.id}
    return render(request, 'files/start_creating_resume_files.html', context)


def resume_file_list_view(request, pk):
    qs = ResumeFile.objects.filter(profile__user=request.user, profile__pk=pk)
    context = {'object_list': qs}
    return render(request, 'files/resumefile_list.html', context)
