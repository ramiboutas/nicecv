from __future__ import annotations

from django.urls import path

from .views import create_cv

app_name = "cvs"

urlpatterns = [
    path("create/", create_cv, name="create"),
]
