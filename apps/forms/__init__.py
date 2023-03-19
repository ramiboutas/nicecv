from __future__ import annotations

from django.apps import AppConfig


class FormsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.forms"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
        from . import tasks  # noqa
