"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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

    # Local apps
    path('pricing/', include('pricing.urls')),
    path('profiles/', include('profiles.urls')),
    path('', include('pages.urls')),

    # Payments
    path("payments/", include("payments.urls")),

]

if settings.DEBUG:
    urlpatterns += [
        # path('__debug__/', include(debug_toolbar.urls)),
        re_path(r'^rosetta/', include('rosetta.urls')),
    ]
