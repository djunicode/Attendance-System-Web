"""
Django settings for attendance_system project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'Attendance/templates')
STATIC_DIR = os.path.join(BASE_DIR, 'Attendance/static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG") == "True"

ALLOWED_HOSTS = config("ALLOWED_HOSTS").replace(" ", "").split(",")


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'Attendance',
    'import_export',
    "corsheaders",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'attendance_system.urls'


# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = config("CORS_ORIGIN_WHITELIST").replace(" ", "").split(",")

# CORS_ALLOW_METHODS = (
#     'GET',
#     'DELETE',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
# )

# CORS_ALLOW_HEADERS = (
#     'accept',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'attendance_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# try:
#     from . import localDBsettings
#     DATABASES = {
#         # create a file attendance_system/localDBsettings.py with the following in it:
#         # default_database = {
#         #     'ENGINE': 'django.db.backends.mysql',
#         #     'NAME': '',
#         #     'USER': '',
#         #     'PASSWORD': '',
#         #     'HOST': 'localhost',
#         #     'PORT': '3306',
#         #     'OPTIONS': {
#         #         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         #     }
#         # }
#         'default': localDBsettings.default_database,
#     }

# except ImportError:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'attendance_system',
#             'USER': 'xyz',
#             'PASSWORD': 'pass@123',
#             'HOST': 'localhost',
#             'PORT': '3306',
#             'OPTIONS': {
#                 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             }
#         },
#     }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated'
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [STATIC_DIR]

# LOGIN_REDIRECT_URL = 'test'
LOGOUT_REDIRECT_URL = 'Attendance:thanks'

LOGIN_URL = 'Attendance:login'

AUTH_USER_MODEL = "Attendance.AppUser"



CORS_ALLOW_ALL_ORIGINS = True