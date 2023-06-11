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
    # My own apps
    path("accounts/", include("core.urls.users")),  # this just for my-account url
    path("plans/", include("core.urls.plans")),
    path("profiles/", include("core.urls.profiles")),
    path("", include("core.urls.home")),
]


# urlpatterns = [
#     path("author-polls/", include("polls.urls", namespace="author-polls")),
#     path("publisher-polls/", include("polls.urls", namespace="publisher-polls")),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
    ]


# Wagtail's serving mechanism (at the ends)
urlpatterns += [path("", include(wagtail_urls))]
