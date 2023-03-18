from __future__ import annotations

from django.apps import AppConfig


class ResumesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.resumes"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
        from . import tasks  # noqa
