# Django settings for lionlist project.

# import from settings/base.py
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': '/usr/local/lionlist.db',                      
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  
        'PORT': '',          
    }
}

MIDDLEWARE_CLASSES += (
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
)

INSTALLED_APPS += (
    # 'django.contrib.admindocs',
)
