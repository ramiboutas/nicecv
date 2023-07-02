from django.urls import path

from ..views.commands import run


urlpatterns = [
    path("command/<str:args>/", run, name="command_run"),
]
