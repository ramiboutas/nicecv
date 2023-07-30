from django.urls import path

from ..views.languages import switch_language


urlpatterns = [
    path("switch-language", switch_language, name="switch_language"),
]
