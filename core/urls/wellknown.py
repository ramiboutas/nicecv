from django.urls import path

from ..views.wellknown import wellknow_admda


urlpatterns = [
    path(".well-known/apple-developer-merchantid-domain-association", wellknow_admda),
]
