from django.urls import path

from .views import download_resume_view


urlpatterns = [
    path("cv-pdf/<int:pk>/", download_resume_view, name="tex_download_resume"),
]
