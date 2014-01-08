# Django settings for lionlist project.

# import unipath
from unipath import Path

# handle paths
PROJECT_DIR = Path(__file__).ancestor(3)
MEDIA_ROOT = PROJECT_DIR.child("media")
#STATIC_ROOT = PROJECT_DIR.child("static")
STATIC_ROOT = ''
STATICFILES_DIRS = (
    PROJECT_DIR.child("static"),
)
TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates")
)

# set admin and managers
ADMINS = (
    ('Ian Zapolsky', 'ianzapolsky@gmail.com'),
)
MANAGERS = ADMINS

# set preferred user model
AUTH_PROFILE_MODULE = 'account.UserProfile'

# set default login and logout redirect urls
LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'

""" DEVELOPMENT EMAIL BACKEND """
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

""" DEVELOPMENT EMAIL PREFERENCES
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
"""

""" GMAIL EMAIL PREFERENCES
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'ianzapolsky@gmail.com'
SERVER_EMAIL = 'ianzapolsky@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ianzapolsky@gmail.com'
EMAIL_HOST_PASSWORD = 'maryvern'
EMAIL_PORT = 587
"""

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# time zone
# more options here:  http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_*(d6ag5%qnxc^@377jp03e0sujaa4&(-enjwbyao@*e$4c0w8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lionlist.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'lionlist.wsgi.application'

INSTALLED_APPS = (

    # lionlist apps
    'account',
    'category',
    'post',
    'course',
    'search',

    # third party apps
    'south',
    'haystack',
    'registration',
    'password_reset',
    'widget_tweaks',

    # django default apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# Haystack Configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

ACCOUNT_ACTIVATION_DAYS = 1

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
