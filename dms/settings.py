"""
Django settings for dms project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nsix7yp-c88ri1t3yb7h2cndb^1nmfha=*sl6dqn^$988s*vhj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
THUMBNAIL_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'widget_tweaks',
    'aplbase',
    'aplhelper',
    'apldistro',
    'aplinventory',
    'apltransaction',
    'aplreport',
    'aplbillship',
    'aplpromotion',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'dms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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


WSGI_APPLICATION = 'dms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbdms',
        'USER': 'root',
        'PASSWORD': 'yanwarsolah',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'ina'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


LEVEL = {'Founder':'F', 'Manager':'M', 'Operator': 'O'}


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'hwijayaa666@gmail.com'
EMAIL_HOST_PASSWORD = 'Acobss12345'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


from django.core.urlresolvers import reverse_lazy, reverse

LOGIN_REDIRECT_URL = reverse_lazy('apldashboard:home')
LOGIN_URL = reverse_lazy('aplaccount:account_login')
# LOGOUT_URL = reverse_lazy('logout')

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Africa/Nairobi'


RAJAONGKIR_KEYAPI = 'e1cf6651edafd48d8ed08c801213f2dd'
RAJAONGKIR_STATE = {'id': 151, 'value': 'Jakarta Barat'}
RAJAONGKIR_URL = 'api.rajaongkir.com'

