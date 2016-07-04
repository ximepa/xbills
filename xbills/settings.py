# -*- encoding: utf-8 -*-
"""
Django settings for xbills project.

Generated by 'django-admin startproject' using Django 1.8.3.

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
SECRET_KEY = '32$i_g^5!4ms7(c+etxce+rj$k_=n4&m6_%$7%)nw6kjqnri#4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASE_ROUTERS = ['xbills.dbrouter.MainDBRouter']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'config',
    'telephone',
    'olltv',
    'dv',
    'ipdhcp',
    'claims',
    'djangorpc',
)

AUTH_USER_MODEL = 'core.Admin'
AUTHENTICATION_BACKENDS = ('core.auth_backend.AuthBackend',)
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.OnlineNowMiddleware',

)

ROOT_URLCONF = 'xbills.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates')],
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

WSGI_APPLICATION = 'xbills.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

DATE_FORMAT = 'Y-m-d'

DATETIME_FORMAT = 'Y-m-d H:s:i'

USE_I18N = True

USE_L10N = False

USE_TZ = False

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
ABONTARIFS = [5, 7, 8, 9, 10, 11]
CPU_WARNING_THRESHOLD = 60
CPU_DANGER_THRESHOLD = 80
MEM_WARNING_THRESHOLD = 60
MEM_DANGER_THRESHOLD = 80
SWAP_WARNING_THRESHOLD = 60
SWAP_DANGER_THRESHOLD = 80
UPTIME_FORMAT = '{days} days {hours}:{minutes}:{seconds}'
PAYMENTS_PER_PAGE = 100
FEES_PER_PAGE = 100
USER_ERRORS_PER_PAGE = 100
IPTV_USERS_PER_PAGE = 100
ABILLSIP = '172.16.7.5'
UNIQUE_MAC = True
COMPANY_NAME = 'Xbills'
PROJECT_VERSION = '0.0.6'
SHOW_VERSION = True
OLLTVAPIVERSION = '2.1.0'
OLLTVUSERAUTH = 'http://dev.oll.tv/ispAPI/auth2/'
OLLTVUSERADDURL = 'http://dev.oll.tv/ispAPI/addUser/'
OLLTVUSERREMOVEURL = 'http://dev.oll.tv/ispAPI/deleteAccount/'
OLLTVUSERLINKINGURL = 'http://dev.oll.tv/ispAPI/changeAccount/'
OLLTVUSERCHANGEEMAILURL = 'http://dev.oll.tv/ispAPI/changeEmail/'
OLLTVUSERLIST = 'http://dev.oll.tv/ispAPI/getUserList/'
OLLTVUSERINFO = 'http://dev.oll.tv/ispAPI/getUserInfo/'
OLLTVCHANGEUSERINFO = 'http://dev.oll.tv/ispAPI/changeUserInfo/'
OLLTVEMILEXISTURL = 'http://dev.oll.tv/ispAPI/emailExists/'
OLLTVACCOUNTEXISTURL = 'http://dev.oll.tv/ispAPI/accountExists/'
OLLTVDEVADDURL = 'http://dev.oll.tv/ispAPI/addDevice/'
OLLTVDEVREMOVEURL = 'http://dev.oll.tv/ispAPI/delDevice/'
OLLTVDEVEXISTURL = 'http://dev.oll.tv/ispAPI/deviceExists/'
OLLTVDEVGETLIST = 'http://dev.oll.tv/ispAPI/getDeviceList/'
OLLTVTPACTIVATEURL = 'http://dev.oll.tv/ispAPI/enableBundle/'
OLLTVTPDEACTIVATEURL = 'http://dev.oll.tv/ispAPI/disableBundle/'
OLLTVGETBUNDLESTATUS = 'http://dev.oll.tv/ispAPI/checkBundle/'
# LOGS
#Add logs to Abills history
ABILLS_EMAIL_LOGS = True

# CHAT && WEBSOCKET
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


try:
    from settings_local import *
except ImportError:
    pass