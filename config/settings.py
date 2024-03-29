import os
from pathlib import Path

import dotenv
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _


# Setup

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

TEX_TEMPLATES_DIR = BASE_DIR / "tex_templates"

ORIGIN_TEXMF_DIR = BASE_DIR / "texmf"

DESTINATION_TEXMF_DIR = Path("/home/rami/texmf")

# Load env vars from .env file
dotenv.load_dotenv(dotenv_path=BASE_DIR / ".env")

# The name of the class to use for starting the test suite.
TEST_RUNNER = "config.test.TestRunner"

# s3 storage
USE_S3 = os.environ.get("USE_S3", "") == "1"

# HTTPS
HTTPS = os.environ.get("HTTPS", "") == "1"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "some-tests-need-a-secret-key")

# SECURITY WARNING: do not run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "") == "1"


INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = ["nicecv.online", "www.nicecv.online", "127.0.0.1", "ramiboutas.com"]


# Application definition

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.forms",
    # My own apps
    "core.CoreConfig",
    "cms.CmsConfig",
    # Wagtail apps
    # "wagtail.contrib.routable_page",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.styleguide",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.forms",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "taggit",
    "modelcluster",
    # Third-party apps
    "wagtail_localize",
    "wagtail_localize.locales",  # This replaces "wagtail.locales"
    # "wagtailmenus",
    "django_extensions",
    "rosetta",
    "modeltranslation",
    "djmoney",
    "djmoney.contrib.exchange",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.linkedin_oauth2",
    "django_htmx",
    "django_cleanup.apps.CleanupConfig",  # https://github.com/un1t/django-cleanup
    "huey.contrib.djhuey",  # https://huey.readthedocs.io/en/latest/django.html
    "crispy_forms",
    "crispy_tailwind",
    "debug_toolbar",
    # "generic_chooser",
    "fontawesomefree",
    "django_minify_html",
    "django_tweets",
    "dbbackup",
    "djstripe",
    "geoip2",
    # "django_browser_reload",
    # "mjml",
    # "birdsong",
]

# Authentication
AUTH_USER_MODEL = "core.User"


# Email Backend

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_USE_TLS = str(os.environ.get("EMAIL_USE_TLS")) == "1"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


MIDDLEWARE = [
    # django middlewares
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # wagtails middlewares
    # "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # third-party middlewares
    "allauth.account.middleware.AccountMiddleware",
    "django_minify_html.middleware.MinifyHtmlMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
    "core.middleware.CountryMiddleware",
]


SESSION_ENGINE = "django.contrib.sessions.backends.db"

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # django
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # wagtail
                "wagtail.contrib.settings.context_processors.settings",
                # core
                "core.context_processors.cv_templates",
                # cms
                "cms.context_processors.cms_menu_pages",
            ],
            "debug": DEBUG,
        },
    },
    {
        "NAME": "tex",
        "BACKEND": "core.tex.backend.TeXEngine",
        "DIRS": [TEX_TEMPLATES_DIR],
        "APP_DIRS": False,
        "OPTIONS": {
            "environment": "core.tex.environment.environment",
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

USE_L10N = True


WAGTAIL_I18N_ENABLED = True


USE_TZ = True

LANGUAGE_COOKIE_NAME = "client_language"

LANGUAGES = WAGTAIL_CONTENT_LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
    ("de", _("German")),
    #  ("fr", _("French")),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


#### Third-party app settings

# Model translation
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

# Currency exchange
OPEN_EXCHANGE_RATES_APP_ID = os.environ.get("OPEN_EXCHANGE_RATES_APP_ID", "")


# allauth

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_LOGOUT_REDIRECT = "/"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
# ACCOUNT_ADAPTER = "core.account_adapter.AccountAdapter"

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_URL = "account_login"

LOGIN_REDIRECT_URL = "profile_list"
LOGOUT_REDIRECT_URL = "/"


# django-allauth (social)

SOCIALACCOUNT_PROVIDERS = {
    # https://django-allauth.readthedocs.io/en/latest/providers.html#google
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": os.environ.get("SOCIALACCOUNT_GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("SOCIALACCOUNT_GOOGLE_SECRET_KEY"),
            "key": "",
        }
    },
    "linkedin_oauth2": {
        "APP": {
            "client_id": os.environ.get("SOCIALACCOUNT_LINKEDIN_CLIENT_ID"),
            "secret": os.environ.get("SOCIALACCOUNT_LINKEDIN_SECRET_KEY"),
            "key": "",
        },
        "SCOPE": ["r_liteprofile", "r_emailaddress", "w_member_social"],
        "PROFILE_FIELDS": [
            "id",
            "first-name",
            "last-name",
            "email-address",
            "picture-url",
            "public-profile-url",
            "openid",
        ],
    },
}


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# static files (whitenoise)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = ((BASE_DIR / "static"),)
LOCAL_MEDIA_URL = "/media/"

# media storage (aws s3)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
if USE_S3:
    AWS_MEDIA_LOCATION = "nicecv/media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"
    MEDIA_STORAGE_BACKEND = "config.storage_backends.MediaRootStorage"
else:
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = LOCAL_MEDIA_URL
    MEDIA_STORAGE_BACKEND = "django.core.files.storage.FileSystemStorage"


STORAGES = {
    "default": {
        "BACKEND": MEDIA_STORAGE_BACKEND,
    },
    "local": {  # not used at the moment: 05.01.2024
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": BASE_DIR / "media",
            "base_url": LOCAL_MEDIA_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


## Backup

# Backups
DBBACKUP_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DBBACKUP_STORAGE_OPTIONS = {
    "access_key": AWS_ACCESS_KEY_ID,
    "secret_key": AWS_SECRET_ACCESS_KEY,
    "bucket_name": AWS_STORAGE_BUCKET_NAME,
    "location": "nicecv/backups/",
    "default_acl": "private",
}


# caching
# Server-side cache settings. Do not confuse with front-end cache.
# https://docs.djangoproject.com/en/stable/topics/cache/
REDIS_UL = os.environ.get("REDIS_TLS_URL", os.environ.get("REDIS_URL"))

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_UL,
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Payments

# Stripe
# live mode
STRIPE_LIVE_MODE = os.environ.get("STRIPE_LIVE_MODE", "") == "1"

# api keys (live)
STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "")
# api keys (test)
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "")
# dj-stripe
DJSTRIPE_WEBHOOK_SECRET = os.environ.get("DJSTRIPE_WEBHOOK_SECRET", "")
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_WEBHOOK_VALIDATION = "retrieve_event"

if STRIPE_LIVE_MODE:
    STRIPE_PUBLIC_KEY = STRIPE_LIVE_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_LIVE_SECRET_KEY
else:
    STRIPE_PUBLIC_KEY = STRIPE_TEST_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_TEST_SECRET_KEY

# currencies

# https://stripe.com/docs/currencies?presentment-currency=DE#presentment-currencies
# Currencies marked with * are not supported by American Express
STANDARD_CURRENCIES = (
    "USD",
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BRL",
    "BSD",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHF",
    "CLP",
    "CNY",
    "COP",
    "CRC",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "GBP",
    "GEL",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "ISK",
    "JMD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KRW",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SOS",
    "SRD",
    "STD",
    "SZL",
    "THB",
    "TJS",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "UYU",
    "UZS",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XCD",
    "XOF",
    "XPF",
    "YER",
    "ZAR",
    "ZMW",
)
# https://stripe.com/docs/currencies?presentment-currency=DE#zero-decimal
ZERO_DECIMAL_CURRENCIES = (
    "BIF",
    "CLP",
    "DJF",
    "GNF",
    "JPY",
    "KMF",
    "KRW",
    "MGA",
    "PYG",
    "RWF",
    "UGX",
    "VND",
    "VUV",
    "XAF",
    "XOF",
    "XPF",
)

# https://stripe.com/docs/currencies?presentment-currency=DE#three-decimal

THREE_DECIMAL_CURRENCIES = ("BHD", "JOD", "KWD", "OMR", "TND")


# Wagtail
WAGTAIL_SITE_NAME = "Nice CV"
WAGTAILADMIN_BASE_URL = "htttps://www.nicecv.online"


# LaTex settings
# LATEX_INTERPRETER = "pdflatex" # pdflatex, latex, xelatex, lualatex
# LATEX_INTERPRETER_OPTIONS = "-interaction=nonstopmode"
# LATEX_GRAPHICSPATH = os.path.join(BASE_DIR, "media") # changed 05.01.2024

TEX_MEDIA_DIR = BASE_DIR / "tex_media"
LATEX_GRAPHICSPATH = [TEX_MEDIA_DIR]


# crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


# translations
DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")

# rosetta
ROSETTA_MESSAGES_PER_PAGE = 50
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_WSGI_AUTO_RELOAD = True

# wagtail-localize

WAGTAILLOCALIZE_MACHINE_TRANSLATOR = {
    "CLASS": "wagtail_localize.machine_translators.deepl.DeepLTranslator",
    "OPTIONS": {"AUTH_KEY": DEEPL_AUTH_KEY},
}


# django-money

CURRENCIES = ("USD", "EUR")


# geoip2

GEOIP_PATH = BASE_DIR / "geoip2dbs"


# shell-plus

SHELL_PLUS = "ipython"


############################
##### project settings #####
############################


# django-tweets
# Consumer Keys
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
# Authentication Tokens
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
# OAuth 2.0 Client ID and Client Secret
TWITTER_CLIENT_ID = os.environ.get("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET = os.environ.get("TWITTER_CLIENT_SECRET")


# Telegram

TELEGRAM_BOT_API_KEY = os.environ.get("TELEGRAM_BOT_API_KEY", "")
TELEGRAM_REPORTING_CHAT_ID = os.environ.get("TELEGRAM_REPORTING_CHAT_ID", "")


# Https for production environment
if HTTPS:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000  # usual: 31536000 (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True


# project settings

SITE_ID = 1

WAGTAIL_INITIAL_SVGS_DIR = BASE_DIR / "initialsvgs"

WAGTAILEMBEDS_RESPONSIVE_HTML = True

WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "svg"]


# https://docs.wagtail.org/en/stable/advanced_topics/customisation/page_editing_interface.html#limiting-features-in-a-rich-text-field
CMS_RICHTEXT_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "ol",
    "ul",
    "link",
    "document-link",
]
