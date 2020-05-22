"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from sys import path
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Add apps  to the PROJECT_ROOT
path.append(os.path.join(PROJECT_ROOT, "backend/apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "24gh!1b0ivo(=g=+9t3qw5--8jp$!cing4-k549m%*7d(z=e)3"
OTP_SECRET_KEY = "1cb4fae17f0dbf7ef32ca012e0837049152349b9378151f28557ed91adc55319"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['217.69.6.52','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'fluent_dashboard',

    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_countries",
    "django_db_logger",
    "mptt",
    "apps.core",
    "apps.entity",
    "apps.kyc",
    "apps.shared",
    "apps.transaction",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': (os.path.join(PROJECT_ROOT, "backend/templates")),
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            'loaders': (
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "backend/static")

# DB LOGGER
DJANGO_DB_LOGGER_ENABLE_FORMATTER = True

# FLUENT - DASHBOARD
ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_THEMING_CSS = 'css/theme.css'
FLUENT_DASHBOARD_DEFAULT_MODULE = 'admin_tools.dashboard.modules.AppList'
FLUENT_DASHBOARD_APP_GROUPS = (

    (_('Users'), {
        'models': (
            'django.contrib.auth.models.User',
        ),
    }),

    (_('Entities and Agents'), {
        'models': (
            'apps.entity.models.entity.*',
            'apps.entity.models.agent.*',
            'apps.shared.models.account*',
        ),
    }),

    (_('Customers , Carteras, Monnamon cards '), {
        'models': (
            'apps.kyc.models.*',
        ),
    }),

    (_('Corridor and Pricing'), {
        'models': (
            'apps.shared.models.price.*',
        ),
    }),

    (_('Country and currency'), {
        'models': (
            'apps.shared.models.country.*',
        ),
    }),

    (_('Transactions'), {
        'models': (
            'apps.transaction.models.*',
        ),
    }),

    (_('Logging'), {
        'models': (
            'django_db_logger.models.*',
            'apps.shared.models.notification.*',
        ),
    }),
)


FLUENT_DASHBOARD_APP_ICONS = {
    'entity/agent': 'users7.png',
    'entity/entity': 'main-page.png',
    'entity/entitysettings': 'cogwheels9.png',

    'shared/corridor': 'globe16.png',

    'transaction/transaction': 'right-arrow7.png',
    'transaction/operation': 'stats2.png',
    'transaction/revenusharingresult': 'img/sharing.png',

    'shared/country': 'world90.png',
    'shared/change': 'share.png',
    'shared/notification': 'file.png',
    'shared/account': 'img/balance.png',

    'kyc/customer': 'multiple25.png',

    'django_db_logger/statuslog': 'archive52.png',

}
