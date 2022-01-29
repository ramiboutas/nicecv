from django.urls import path

from .views import download_resume_view, download_coverletter_view




urlpatterns = [
    path('download-resume/<uuid:pk>/', download_resume_view, name='texfiles_download_resume'),
    path('download-coverletter/<uuid:pk>/', download_coverletter_view, name='texfiles_download_coverletter'),
]
