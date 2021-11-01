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

from pages.views import HomePageView


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('django.contrib.auth.urls')),

    path('i18n/', include('django.conf.urls.i18n')),

    path('', include('pages.urls')),

]

# Local apps
# urlpatterns += i18n_patterns(path('', include('pages.urls')))

if settings.DEBUG:
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),


if 'rosetta' in settings.INSTALLED_APPS and settings.DEBUG:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
