import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path


urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # i18n
    path("i18n/", include("django.conf.urls.i18n")),
    # User management
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),  # this just for my-account url
    # My own apps
    path("", include("core.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("profiles/", include("profiles.urls")),
    path("texfiles/", include("texfiles.urls")),
    # translation tool
    path("rosetta/", include("rosetta.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
