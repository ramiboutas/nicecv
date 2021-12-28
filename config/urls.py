import debug_toolbar

from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # i18n 
    path('i18n/', include('django.conf.urls.i18n')),

    # User management
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')), # this just for my-account url

    # My own apps
    path('pricing/', include('pricing.urls')),
    path('profiles/', include('profiles.urls')),
    path('', include('pages.urls')),

    # Payments
    path("payments/", include("payments.urls")),
    # dj-stripe
    # path("stripe/", include("djstripe.urls", namespace="djstripe")),

    # translation tool
    path('rosetta/', include('rosetta.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
