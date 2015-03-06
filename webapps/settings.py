"""
Django settings for webapps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Parse database configuration from $DATABASE_URL
import os
import ConfigParser
import dj_database_url


#import os
import psycopg2
import urlparse

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES={}

#DATABASES['default'] =  dj_database_url.config(default='postgres://testadmin:testing@localhost/django_db')

#DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# This application object is used by the development server
# as well as any WSGI server configured to use this file.

WSGI_APPLICATION = 'webapps.wsgi.application'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5^gf54zmd+ha2fs@)8gq%m^-#i*#yztykp45pjd!v9^i-d)7h='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = ['limitless-falls-6527.herokuapp.com']


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'socialnetwork'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'webapps.urls'

# Used by the authentication system for the private-todo-list application.
# URL to use if the authentication system requires a user to log in.
LOGIN_URL = '/socialnetwork/login'

# Default URL to redirect to after a user logs in.
LOGIN_REDIRECT_URL = '/socialnetwork/'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

#STATIC_URL = '/static/'

MEDIA_URL = '/pictures/'


# Email
#config = ConfigParser.ConfigParser()
#config.read("../config.ini")

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.andrew.cmu.edu'
EMAIL_HOST_USER = os.environ.get('USER')
EMAIL_HOST_PASSWORD = os.environ.get('PASSWORD')
EMAIL_PORT = 465

print 'EMAIL_HOST',EMAIL_HOST+':'+str(EMAIL_PORT)
print 'EMAIL_HOST_USER',EMAIL_HOST_USER

import dj_database_url

DATABASES['default'] =  dj_database_url.config()
