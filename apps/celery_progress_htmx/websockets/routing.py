from django.urls import re_path

from apps.celery_progress_htmx.websockets import consumers

try:
    progress_consumer = (
        consumers.ProgressConsumer.as_asgi()
    )  # New in Channels 3, works similar to Django's .as_view()
except AttributeError:
    progress_consumer = (
        consumers.ProgressConsumer
    )  # Channels 3 not installed, revert to Channels 2 behavior

urlpatterns = [
    re_path(r"^ws/progress/(?P<task_id>[\w-]+)/?$", progress_consumer),
]
