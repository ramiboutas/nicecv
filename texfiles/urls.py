from django.urls import path

from .views import download_resume_view, download_coverletter_view




urlpatterns = [
    path('your-cv/<int:pk>/', download_resume_view, name='texfiles_download_resume'),
    path('download-coverletter/<int:pk>/', download_coverletter_view, name='texfiles_download_coverletter'),
]
