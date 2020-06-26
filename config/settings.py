import os
from datetime import timedelta

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'corsheaders',
    'drf_yasg',
    'django_nose',
    'django_extensions',
    'apps.common',
    'apps.users',
    'apps.blog',
    'apps.task',
    'TaskManager',
    'rest_framework.authtoken',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.common.middlewares.ApiMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["TaskManager/templates/"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
    'cache-control'
)

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%SZ",
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'apps.common.exceptions.custom_exception_handler'

}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

ELASTICSEARCH_INDEX_NAMES = {
    'TaskManager.search_indexes': 'search_indexes',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

FIXTURE_DIRS = (
    'fixtures/',
)

DEFAULT_LANG = "ro"
LANGUAGES = [
    (DEFAULT_LANG, _('Romanian')),
    ('ru', _('Russian')),
    ('en', _('English')),
]
DICT_LANG = {}
for lang_key, lang_name in LANGUAGES:
    DICT_LANG[lang_key] = None

LOCALE_PATHS = (
    BASE_DIR + '/locales',
)

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATE_FORMAT = "%Y-%m-%d %H:%m"

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=TaskManager',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')%1nllc!l^6lnwjgmA7tfs9@%9axr_^=^h%krzs&keih+!j+#q'

WSGI_AUTO_RELOAD = True

DEBUG = True

DEBUG_LEVEL = "INFO"

LOGIN_URL = '/TaskManager/login'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]- %(message)s'}

    },
    'handlers': {
        'console': {
            'level': DEBUG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'info': {
            'handlers': ["console"],
            'level': DEBUG_LEVEL,
            'propagate': True
        },
        'django': {
            'handlers': ['console'],
            'level': DEBUG_LEVEL,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': DEBUG_LEVEL,
            'propagate': True,
        }
    },
}

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'DjangoDB',

        'USER': 'postgres',

        'PASSWORD': 'qwe123',

        'HOST': '192.168.88.97',

        'PORT': '5432',

    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }
SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),

    'AUTH_HEADER_TYPES': ('Bearer', 'Token'),

}

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
