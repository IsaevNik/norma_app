import os
from cloghandler import ConcurrentRotatingFileHandler

BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))

SECRET_KEY = '=abo0)z#b+e+5-!0csj$(nsrx*ef8rt0#0k=)3cgbv@wm*!z^3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'rest_framework.authtoken',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'norma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'norma.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'norma',
            'USER': 'norma',
            'PASSWORD': 'norma',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

MERCHAND_ID = '51227'
SECRET1 = 'gowxko6r'
SECRET2 = 'lbsrwwmi'
PAYMENT_URL = 'https://www.free-kassa.ru/merchant/cash.php'

NORMA_BOT_TOKEN = 'afcf3e83-42d0-4540-a26b-6d4ae820c1c8'
BOT_URL = 'http://127.0.0.1:8888/'

LOG_PATH = os.path.join(BASE_DIR, 'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '%(asctime)s [%(name)s.%(levelname)s] '
                      '%(message)s '
                      '(%(filename)s:%(lineno)d)',
            'datefmt': "%Y.%m.%d %H:%M:%S",
        },
    },
    'handlers': {
        'main_handler': {
            'level': 'INFO',
            'filename': os.path.join(LOG_PATH, 'app.log'),
            'class': 'logging.handlers.ConcurrentRotatingFileHandler',
            'formatter': 'main_formatter',
            'maxBytes': 2097152, # 2MB
            'backupCount': 10
        }
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['main_handler', ],
        },
        'payment': {
            'level': 'INFO',
            'handlers': ['main_handler', ],
        }
    }
}
