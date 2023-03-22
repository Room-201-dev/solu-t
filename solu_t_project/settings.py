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


DEBUG = False

SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True
SECRET_KEY = '&0=+d!3@h+))wz8byut_0=)2t&$o_x4wj@o3r^@9&rtd&22*f+'

DATE_INPUT_FORMATS += ['%Y/%m/%d']
DATETIME_INPUT_FORMATS += ('%Y/%m/%d',)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'towacast.labor.shift@gmail.com'
EMAIL_HOST_PASSWORD = 'zxjeilhlluwhbdtl'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'towacast.labor.shift@gmail.com'

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

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

USE_L10N = True

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

try:
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

    # Extra places for collectstatic to find static files.
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, "staticfiles")
    # ]
    # SECRET_KEY = os.environ['SECRET_KEY']

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
            default='postgres://rddrgxkeodjqfn:24b9360ec462eeee3f39f37c0bd11e1b59b1c9b3e590c2c15d5d74f342b06e7c@ec2-100-26-39-41.compute-1.amazonaws.com:5432/domjaglaeugos')
    }
    ALLOWED_HOSTS = ['.herokuapp.com']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

# 'solu-t.herokuapp.com',
# postgres://mpotwowbeuzlgm:08022d45dd46c697d3add0daea9dde85e521f4352c902aa51435e61546bac78c@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d75ouve3ekkcpm