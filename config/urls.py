import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path


urlpatterns = [
    # Django
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    
    # Third-party apps
    path("accounts/", include("allauth.urls")),
    path("rosetta/", include("rosetta.urls")),

    # My own apps
    path("accounts/", include("accounts.urls")),  # this just for my-account url
    path("subscriptions/", include("subscriptions.urls")),
    path("profiles/", include("profiles.urls")),
    path("texfiles/", include("texfiles.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls)),]