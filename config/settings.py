
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get('DEBUG')) == '1'
PRODUCTION = str(os.environ.get('PRODUCTION')) == '1'

INTERNAL_IPS = ['127.0.0.1', 'localhost',]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party apps
    'rosetta',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_htmx',
    'djstripe',


    # Local
    'accounts.apps.AccountsConfig',
    'pages.apps.PagesConfig',
    'pricing.apps.PricingConfig',
    'profiles.apps.ProfilesConfig',

]

# Authentication
AUTH_USER_MODEL = 'accounts.CustomUser'

# allauth
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_LOGOUT_REDIRECT = 'home'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


# Email Backend

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = str(os.environ.get('EMAIL_USE_TLS')) == '1'
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]



if DEBUG:
    INSTALLED_APPS  += ['debug_toolbar',]
    MIDDLEWARE  += ['debug_toolbar.middleware.DebugToolbarMiddleware',]


if PRODUCTION:
    ALLOWED_HOSTS += ['nicecv.online', 'www.nicecv.online', '207.154.205.99', 'localhost', '127.0.0.1']
    # https
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 3600 # usual: 31536000 (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True



ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.nicecv',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Database
USE_SQLITE3_DB = str(os.environ.get('USE_SQLITE3_DB')) == '1'

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_TESTS_DB = os.environ.get('POSTGRES_TESTS_DB')


if USE_SQLITE3_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
            'TEST': {
             'NAME': 'test_db',
             },
        }
    }



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

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

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (str(BASE_DIR.joinpath('static_dev')),)
STATIC_ROOT = str(BASE_DIR.joinpath('static')) # for production

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


 # Message tags
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}




# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Payments

# Stripe

STRIPE_LIVE_MODE = str(os.environ.get('STRIPE_LIVE_MODE')) == '1'
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")
DJSTRIPE_WEBHOOK_SECRET = os.environ.get("DJSTRIPE_WEBHOOK_SECRET")
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"


# payments (django-payments app)
# https://django-payments.readthedocs.io/en/latest/install.html
# PAYMENT_HOST = 'localhost:8000'
# PAYMENT_USES_SSL = False
# PAYMENT_MODEL = 'pricing.Payment'
# PAYMENT_VARIANTS = {'default': ('payments.dummy.DummyProvider', {})}



# SEO, Meta data & Naming

SITE_NAME = _('Nice CV')
META_KEYWORDS = _('Enter meta keywords here')
META_DESCRIPTION = _('Enter meta description here')

#  pricing site
DEFAULT_PRICING_MONTH = 6
MONTH_PRICING = (
# months, price, saving
    (1, 12.00, 0),
    (2, 21.50, 2.5),
    (3, 28.90, 7.1),
    (4, 34.1, 13.9),
    (5, 38.2, 21.8),
    (6, 41.5, 30.5),
    (7, 44.2, 39.8),
    (8, 46.7, 49.3),
    (9, 48.8, 59.2),
    (10, 50.70, 69.3),
    (11, 52.70, 79.3),
    (12, 54.00, 90),
)
DEFAULT_PRICING_PRICE = MONTH_PRICING[DEFAULT_PRICING_MONTH][1]
DEFAULT_PRICING_SAVING = MONTH_PRICING[DEFAULT_PRICING_MONTH][2]


# Redirects after login & logout

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
