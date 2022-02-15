from django.urls import path

from .views import start_creating_resume_files_view, resume_file_list_view


urlpatterns = [
    path('start-creating-resumes/<uuid:pk>', start_creating_resume_files_view, name='files_resume_file_list'),
    path('resumes/<uuid:pk>', resume_file_list_view, name='files_resume_file_list'),
    # path('pdf/<int:pk>/', download_pdf_view, name='files_download_pdf'),
    # path('download-coverletter/<int:pk>/', download_coverletter_view, name='files_download_coverletter'),
]
