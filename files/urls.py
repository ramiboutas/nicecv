from django.urls import path, re_path

from .views import generate_resumes_view, resume_creation_status_view
from .views import resume_file_list_view


urlpatterns = [
    path('generate-resumes/<uuid:pk>/', generate_resumes_view, name='files_generate_resumes'),
    # re_path('task-result/(?P<task_id>[\w-]+)/<uuid:pk>/', resume_creation_status_view, name='files_resume_creation_status'),
    path('task-result/<str:task_id>/<uuid:pk>/', resume_creation_status_view, name='files_resume_creation_status'),
    path('resumes/<uuid:pk>/', resume_file_list_view, name='files_resume_file_list'),
    # path('pdf/<int:pk>/', download_pdf_view, name='files_download_pdf'),
    # path('download-coverletter/<int:pk>/', download_coverletter_view, name='files_download_coverletter'),
]
