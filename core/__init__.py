from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "00 Core"

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
