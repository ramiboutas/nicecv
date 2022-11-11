import os
from pathlib import Path
import sys
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


import dotenv

# Setup

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Load env vars from .env file if not testing
try:
    command = sys.argv[1]
except IndexError:  # pragma: no cover
    command = "help"

if command != "test":  # pragma: no cover
    dotenv.load_dotenv(dotenv_path=BASE_DIR / ".env")


# Production
PRODUCTION = os.environ.get("PRODUCTION", "") == "1"

# Use Postgres (otherwise Sqlite)
USE_POSTGRES = os.environ.get("USE_POSTGRES", "") == "1"

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', "some-tests-need-a-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get('DEBUG')) == '1'
PRODUCTION = str(os.environ.get('PRODUCTION')) == '1'

INTERNAL_IPS = ['127.0.0.1', 'localhost',]

ALLOWED_HOSTS = ['nicecv.online', 'www.nicecv.online', '207.154.205.99', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # My own apps
    'accounts.apps.AccountsConfig',
    'pages.apps.PagesConfig',
    'pricing.apps.PricingConfig',
    'profiles.apps.ProfilesConfig',
    'payments.apps.PaymentsConfig',
    'texfiles.apps.TexfilesConfig',
    # 'files.apps.FilesConfig',

    # Third-party apps
    'rosetta',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.linkedin',
    'django_htmx',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_tex',
    'celery_progress_htmx',
    'django_celery_results',
    'analytical',
    # 'djstripe',

    # Tools for debug
    'debug_toolbar',

]

# Authentication
AUTH_USER_MODEL = 'accounts.CustomUser'

# allauth
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_LOGOUT_REDIRECT = 'home'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Provider specific settings
SOCIALACCOUNT_GOOGLE_CLIENT_ID = os.environ.get('SOCIALACCOUNT_GOOGLE_CLIENT_ID') # my own variable
SOCIALACCOUNT_GOOGLE_SECRET_KEY = os.environ.get('SOCIALACCOUNT_GOOGLE_SECRET_KEY') # my own variable

SOCIALACCOUNT_PROVIDERS = {
    # https://django-allauth.readthedocs.io/en/latest/providers.html#google
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': SOCIALACCOUNT_GOOGLE_CLIENT_ID,
            'secret': SOCIALACCOUNT_GOOGLE_SECRET_KEY,
            'key': ''
        }
    },
    # https://django-allauth.readthedocs.io/en/latest/providers.html#linkedin
    # 'linkedin': {
    #     'SCOPE': [
    #         'r_basicprofile',
    #         'r_emailaddress'
    #     ],
    #     'PROFILE_FIELDS': [
    #         'id',
    #         'first-name',
    #         'last-name',
    #         'email-address',
    #         'picture-url',
    #         'public-profile-url',
    #     ]
    # }
}


# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = str(os.environ.get('EMAIL_USE_TLS')) == '1'
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST

MIDDLEWARE = [
    # django middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # third-party middlewares
    'django_htmx.middleware.HtmxMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # django context processors
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # my own context processors
                'utils.context_processors.nicecv',
                'texfiles.context_processors.texfiles',
            ],
        },
    },
    {
        'NAME': 'tex',
        'BACKEND': 'django_tex.engine.TeXEngine',
        'DIRS': (BASE_DIR.joinpath('tex_templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'texfiles.environment.my_environment',
        }
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database

# Database
if USE_POSTGRES:
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "")
    POSTGRES_TESTS_DB = os.environ.get("POSTGRES_TESTS_DB", "")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
            "TEST": {
                "NAME": "test_db",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_COOKIE_NAME = 'client_language'

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
    ('de', _('German')),
    ('fr', _('French')),
    ('pt', _('Portuguese')),
    ('it', _('Italian')),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = (str(BASE_DIR.joinpath('static_dev')),)
STATIC_ROOT = str(BASE_DIR.joinpath('static')) # for production

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
# Media files
MEDIA_ROOT = BASE_DIR.joinpath('media')
MEDIA_URL = '/media/'

# Message tags
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Payments

# Stripe - general
STRIPE_LIVE_MODE = str(os.environ.get('STRIPE_LIVE_MODE')) == '1'

# Stripe - live keys
STRIPE_LIVE_PUBLIC_KEY=os.environ.get("STRIPE_LIVE_PUBLICKEY")
STRIPE_LIVE_SECRET_KEY=os.environ.get("STRIPE_LIVE_SECRET_KEY")
STRIPE_LIVE_WEBHOOK_SECRET=os.environ.get("STRIPE_LIVE_WEBHOOK_SECRET")

# Stripe - test keys
STRIPE_TEST_PUBLIC_KEY=os.environ.get("STRIPE_TEST_PUBLIC_KEY")
STRIPE_TEST_SECRET_KEY=os.environ.get("STRIPE_TEST_SECRET_KEY")
STRIPE_TEST_WEBHOOK_SECRET=os.environ.get("STRIPE_TEST_WEBHOOK_SECRET")

# Stripe - depending on the STRIPE_LIVE_MODE, we select to test keys or production keys
if STRIPE_LIVE_MODE:
    STRIPE_PUBLIC_KEY = STRIPE_LIVE_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_LIVE_SECRET_KEY
    STRIPE_WEBHOOK_SECRET = STRIPE_LIVE_WEBHOOK_SECRET
else:
    STRIPE_PUBLIC_KEY = STRIPE_TEST_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_TEST_SECRET_KEY
    STRIPE_WEBHOOK_SECRET = STRIPE_TEST_WEBHOOK_SECRET


# addional for dj-stripe
DJSTRIPE_WEBHOOK_SECRET = STRIPE_WEBHOOK_SECRET
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# PayPal
# Keys & stuff to include

# Coinbase
# Keys & stuff to include


# SEO, Meta data & Naming
# 'utils.context_processors.nicecv
SITE_NAME = _('Nice CV')
META_KEYWORDS = _('nice cv, professional, resume, jobs, good impressions')
META_DESCRIPTION = _('Nice CV online lets you to create high quality CVs and related services')


# profile settings

RESUME_IMAGE_DIRECTORY = 'resumes/images'
RESUME_PDF_DIRECTORY = 'resumes/pdfs'
RESUME_IMAGE_FORMAT = 'jpg'


# LaTex settings
# LATEX_INTERPRETER = 'pdflatex' # pdflatex, latex, xelatex, lualatex
# LATEX_INTERPRETER_OPTIONS = '-interaction=nonstopmode'
LATEX_GRAPHICSPATH = os.path.join(BASE_DIR, 'media')

# celery
# CELERY_ACCEPT_CONTENT = ['json'] # prod issue: https://github.com/celery/celery/issues/3047
# CELERY_ACCEPT_CONTENT = ['pickle', 'json'] # https://stackoverflow.com/questions/47141842/celery-traceback-encoding-error
# CELERY_BROKER_URL = 'redis://95.90.192.83:6379/0' #raspberry pi
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'django-db'


# crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# analytics
CLICKY_SITE_ID = os.environ.get("CLICKY_SITE_ID")
GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = os.environ.get("GOOGLE_ANALYTICS_GTAG_PROPERTY_ID", "G-XXXXXXXX")

# https://stackoverflow.com/questions/70705968/how-to-test-a-url-in-django
APPEND_SLASH: bool = True # by default

# General stuff depending on debug and production
if PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000 # usual: 31536000 (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
