import debug_toolbar
from allauth.account import views as account_views
from allauth.socialaccount import views as socialaccount_views
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

urlpatterns = [
    ##### Django admin
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    ##### Wagtail admin
    path("wagtail/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    ##### Third-party apps
    # allauth
    path("", include("allauth.urls")),
    # stripe
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    # rosetta
    path("rosetta/", include("rosetta.urls")),
    # sitemap
    path("sitemap.xml", sitemap),
    # core app
    path("", include("core.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        # path("__reload__/", include("django_browser_reload.urls")),
    ]

# Wagtail's serving mechanism (at the ends)
urlpatterns += [path("", include(wagtail_urls))]
