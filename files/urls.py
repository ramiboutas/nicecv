from django.urls import path

from .views import resumefile_list_view


urlpatterns = [
    path('<uuid:pk>/resumes', resumefile_list_view, name='files_resume_file_list')
    # path('pdf/<int:pk>/', download_pdf_view, name='files_download_pdf'),
    # path('download-coverletter/<int:pk>/', download_coverletter_view, name='files_download_coverletter'),
]
