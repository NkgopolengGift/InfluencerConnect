from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')

TIKTOK_CLIENT_SECRET = config('TIKTOK_CLIENT_SECRET')
TIKTOK_CLIENT_KEY = config('TIKTOK_CLIENT_KEY')

CHAT_ENGINE_PROJECT_ID = config('CHAT_ENGINE_PROJECT_ID')
CHAT_ENGINE_PRIVATE_KEY = config('CHAT_ENGINE_PRIVATE_KEY')

PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')

ALLOWED_HOSTS = [
    '*'
]

# Application definition

INSTALLED_APPS = [
    'channels',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_htmx',
    'baseApplication.apps.BaseapplicationConfig',
    'rest_framework',
    
]
#For Login
AUTH_USER_MODEL = 'baseApplication.User'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('127.0.0.1', 6379)],
#         },
#     },
# }
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'InfluencerConnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'InfluencerConnect.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'InfluencerConnectDB',
#         'USER': 'postgres',
#         'PASSWORD': config('DATABASE_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
#Database outside
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'influencerconnectdb_es0o',
        'USER': 'influencerconnectdb_es0o_user',
        'PASSWORD': 'TiHImOMsz8T0ff78PanpVVoAi6ac6WTL',
        'HOST': 'dpg-cptnh3o8fa8c738nf190-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}
#Database inside


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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'fakelorrainebianca@gmail.com'
EMAIL_HOST_PASSWORD = '@Lorraine2020'
DEFAULT_FROM_EMAIL = 'fakelorrainebianca@gmail.com'

CSRF_TRUSTED_ORIGINS=['https://5362-168-172-120-67.ngrok-free.app']