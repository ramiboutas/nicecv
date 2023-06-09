import os
from pathlib import Path

import dotenv
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Setup

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_DIR = BASE_DIR / "temp"

TESTS_TEMP_DIR = TEMP_DIR / "tests"

BASE_TEX_DIR = BASE_DIR / "templates" / "tex"

CV_TEX_DIR = BASE_TEX_DIR / "cvs"

# Load env vars from .env file
dotenv.load_dotenv(dotenv_path=BASE_DIR / ".env")

# The name of the class to use for starting the test suite.
TEST_RUNNER = "config.test.TestRunner"

# Use Digital Ocean Spaces service (Storage)
USE_SPACES = os.environ.get("USE_SPACES", "") == "1"

# HTTPS
HTTPS = os.environ.get("HTTPS", "") == "1"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "some-tests-need-a-secret-key")

# SECURITY WARNING: do not run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "") == "1"


INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = [
    "nicecv.online",
    "www.nicecv.online",
    "127.0.0.1",
    "testserver",
    "nicecv.local",
]


# Application definition

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
    # My own apps
    # "apps.forms.apps.FormsConfig",
    "apps.accounts",
    "apps.cvs",
    "apps.core",
    "apps.plans",
    "apps.profiles",
    "apps.proxies",
    "apps.tex",
    "apps.celery_progress_htmx",  # Actually a thid party but adapted
    # Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "taggit",
    "modelcluster",
    # Third-party apps
    "django_extensions",
    "rosetta",
    "modeltranslation",
    "djmoney",
    "djmoney.contrib.exchange",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.linkedin",
    "django_htmx",
    "django_tex",
    "django_celery_results",
    "djstripe",
    "django_cleanup.apps.CleanupConfig",  # https://github.com/un1t/django-cleanup
    "crispy_forms",
    "crispy_tailwind",
    "debug_toolbar",
    "django_browser_reload",
]

# Authentication
AUTH_USER_MODEL = "accounts.CustomUser"

# allauth
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_LOGOUT_REDIRECT = "core:home"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"


# Provider specific settings
SOCIALACCOUNT_GOOGLE_CLIENT_ID = os.environ.get(
    "SOCIALACCOUNT_GOOGLE_CLIENT_ID"
)  # my own variable
SOCIALACCOUNT_GOOGLE_SECRET_KEY = os.environ.get(
    "SOCIALACCOUNT_GOOGLE_SECRET_KEY"
)  # my own variable

SOCIALACCOUNT_PROVIDERS = {
    # https://django-allauth.readthedocs.io/en/latest/providers.html#google
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": SOCIALACCOUNT_GOOGLE_CLIENT_ID,
            "secret": SOCIALACCOUNT_GOOGLE_SECRET_KEY,
            "key": "",
        }
    },
}


# Email Backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_USE_TLS = str(os.environ.get("EMAIL_USE_TLS")) == "1"
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST

MIDDLEWARE = [
    # django middlewares
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # wagtails middlewares
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # third-party middlewares
    "django_htmx.middleware.HtmxMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]


SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # django context processors
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # project context processors
                "config.project.context_processors",
            ],
            "debug": DEBUG,
        },
    },
    {
        "NAME": "tex",
        "BACKEND": "django_tex.engine.TeXEngine",
        "DIRS": [BASE_TEX_DIR],
        "APP_DIRS": False,
        "OPTIONS": {
            "environment": "apps.tex.environment.tex_environment",
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "testing_db"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "TEST": {
            "NAME": "test_db",
        },
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGE_COOKIE_NAME = "client_language"

LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
    ("de", _("German")),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Model translation
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

# Currency exchange
OPEN_EXCHANGE_RATES_APP_ID = os.environ.get("OPEN_EXCHANGE_RATES_APP_ID", "")

# geoip2
GEOIP_PATH = BASE_DIR / "geoip2dbs"


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


if USE_SPACES:  # pragma: no cover
    # Stuff that could be useful (comments):
    # AWS_LOCATION = f"https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com"
    # MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com/{AWS_MEDIA_LOCATION}/" # it worked
    # MEDIA_URL = f"https://{AWS_s3_endpoint_url}/{AWS_MEDIA_LOCATION}/"
    # STATIC_URL = f"https://{AWS_s3_endpoint_url}/{AWS_STATIC_LOCATION}/"

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"
    AWS_S3_CUSTOM_DOMAIN = "ramiboutas.fra1.cdn.digitaloceanspaces.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400", "ACL": "public-read"}

    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    DEFAULT_FILE_STORAGE = "config.storage.MediaRootStorage"
    STATICFILES_STORAGE = "config.storage.StaticRootStorage"

    AWS_STATIC_LOCATION = "nicecv-static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"
    STATIC_ROOT = f"{AWS_STATIC_LOCATION}/"

    AWS_MEDIA_LOCATION = "nicecv-media"

    MEDIA_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"
    MEDIA_ROOT = f"{AWS_MEDIA_LOCATION}/"

else:  # pragma: no cover
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Message tags

MESSAGE_TAGS = {messages.ERROR: "danger"}


# caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Payments

# Stripe (dj-stripe)
STRIPE_LIVE_MODE = os.environ.get("STRIPE_LIVE_MODE", "") == "1"
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "")
DJSTRIPE_WEBHOOK_SECRET = os.environ.get("DJSTRIPE_WEBHOOK_SECRET", "")
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_WEBHOOK_VALIDATION = "retrieve_event"

# Wagtail
WAGTAIL_SITE_NAME = "Nice CV"
WAGTAILADMIN_BASE_URL = "htttps://www.nicecv.online"


# LaTex settings
# LATEX_INTERPRETER = "pdflatex" # pdflatex, latex, xelatex, lualatex
# LATEX_INTERPRETER_OPTIONS = "-interaction=nonstopmode"
LATEX_GRAPHICSPATH = os.path.join(BASE_DIR, "media")

# celery
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "django-db"


# crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


# analytics
GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = os.environ.get(
    "GOOGLE_ANALYTICS_GTAG_PROPERTY_ID", "G-XXXXXXXX"
)

# rosseta

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


# Https for production environment
if HTTPS:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000  # usual: 31536000 (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True


# html form elements

FORM_ATTRIBUTES = {
    "textinput": {
        "class": "px-2 w-full rounded-md border-transparent focus:border-transparent focus:ring-0",
        "x_bind_class": "active ? 'bg-indigo-200' : ''",
        "hx_trigger": "keyup changed delay:1s, change",
        "label": {
            "class": "absolute -top-2 left-2 inline-block px-1 text-xs font-medium text-gray-400",
            "x_bind_class": "active ? ' bg-indigo-200' : ''",
        },
    },
    "rangeinput": {
        "class": "w-full",
    },
    "checkbox": {
        "class": "h-4 w-4 rounded border-indigo-600 focus:ring-indigo-400 accent-indigo-600",
    },
    "fileinput": {
        "class": """block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"""
    },
}

# project settings

CREATE_INITIAL_PLAN_OBJECTS = False
CREATE_INITIAL_CV_TEX_OBJECTS = True
