"""
Django settings for solu_t_project project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.conf.global_settings import DATE_INPUT_FORMATS, DATETIME_INPUT_FORMATS
import django_heroku
import dj_database_url
from socket import gethostname

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

SECRET_KEY = '&0=+d!3@h+))wz8byut_0=)2t&$o_x4wj@o3r^@9&rtd&22*f+'

DEBUG = False

SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True

ALLOWED_HOSTS = ['*']

DATE_INPUT_FORMATS += ['%Y/%m/%d']
DATETIME_INPUT_FORMATS += ('%Y/%m/%d',)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'towacast.labor.management@gmail.com'
EMAIL_HOST_PASSWORD = 'puvmuufmogosgcqe'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'towacast.labor.management@gmail.com'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'solu_t',
    'accounts',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'mdeditor',
]

BOOTSTRAP4 = {
    'include_jquery': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'solu_t_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'solu_t/templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'bootstrap4.templatetags.bootstrap4',
            ],
        },
    },
]

WSGI_APPLICATION = 'solu_t_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = False

USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1
LOGIN_REDIRECT_URL = "login/"
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTH_USER_MODEL = 'solu_t.CustomUser'

X_FRAME_OPTIONS = 'SAMEORIGIN'
MDEDITOR_CONFIGS = {
    'default': {
        'language': 'en',
    }
}

try:
    # 存在する場合、ローカルの設定読み込み
    from .settings_local import *
except ImportError:
    pass

if not DEBUG:
    # Heroku settings

    # staticの設定

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Static files (CSS, JavaScript, Images)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'

    # # Extra places for collectstatic to find static files.
    # STATICFILES_DIRS = (
    #     os.path.join(BASE_DIR, 'static'),
    # )

    MIDDLEWARE += [
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ]

    # HerokuのConfigを読み込み
    django_heroku.settings(locals())

hostname = gethostname()

if "kojimakaiMacBook-Pro" in hostname:
    # デバッグ環境
    # DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ALLOWED_HOSTS = ['*']
else:
    # 本番環境
    # DEBUG = False
    import dj_database_url

    db_from_env = dj_database_url.config()
    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://mpotwowbeuzlgm:08022d45dd46c697d3add0daea9dde85e521f4352c902aa51435e61546bac78c@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d75ouve3ekkcpm')
    }
    ALLOWED_HOSTS = ['*']
