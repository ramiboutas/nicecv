from django.urls import path

from .views import download_resume_view

app_name = "tex"

urlpatterns = [
    path("cv-pdf/<int:pk>/", download_resume_view, name="download_resume"),
]
