import debug_toolbar

from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # i18n
    path('i18n/', include('django.conf.urls.i18n')),

    # User management
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')), # this just for my-account url

    # My own apps
    path('', include('pages.urls')),
    path('pricing/', include('pricing.urls')),
    path('profiles/', include('profiles.urls')),
    path('pdfs/', include('texfiles.urls')),
    path("payments/", include("payments.urls")),

    # Payments
    # dj-stripe
    # path("stripe/", include("djstripe.urls", namespace="djstripe")),

    # translation tool
    path('rosetta/', include('rosetta.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
