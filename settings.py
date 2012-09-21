# coding: utf-8
import unclebob

from os.path import dirname, abspath, join
LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (u'Marcel Nicolay', 'marcelnicolay@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': LOCAL_FILE('shipping.sqlite3'),
    },
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = LOCAL_FILE('static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages"
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
     LOCAL_FILE('templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'shipping',
    'south',
    'unclebob',
)

SOUTH_TESTS_MIGRATE = True
TEST_RUNNER = 'unclebob.runners.Nose'
unclebob.take_care_of_my_tests()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
       'simple': {
            'format': '%(levelname)s %(message)s'
        }
     },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
            'filters': []
        },
    }
}
