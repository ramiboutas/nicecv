from __future__ import annotations

from django.urls import path

from .views import create_cv

app_name = "cvs"

urlpatterns = [
    path("create/<uuid:profile_id>/<id:tex_id>/", create_cv, name="cv-create"),
]
