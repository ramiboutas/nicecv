import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # Django
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # Wagtail
    path("wagtail/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # Third-party apps
    path("accounts/", include("allauth.urls")),
    path("rosetta/", include("rosetta.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    # core app
    path("", include("core.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
    ]

# urlpatterns = urlpatterns + i18n_patterns(
#     # path("search/", search_views.search, name="search"),
#     # For anything not caught by a more specific rule above, hand over to
#     # Wagtail's page serving mechanism. This should be the last pattern in
#     # the list:
#     path("", include(wagtail_urls)),
#     # Alternatively, if you want Wagtail pages to be served from a subpath
#     # of your site, rather than the site root:
#     #    path("pages/", include(wagtail_urls)),
# )
# Wagtail's serving mechanism (at the ends)
urlpatterns += [path("", include(wagtail_urls))]
