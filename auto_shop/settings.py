"""
Django settings for auto_shop project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-votre-cle-secrete-ici'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
# auto_shop/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Ajouter ceci
    'rest_framework.authtoken',  # Pour l'authentification par token
    'vehicles',
    'channels',
    'corsheaders',
    'accounts',
    'orders',
    'payments', 
    'chat',
    'reviews',
    'favorites',
    'blog',
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Pour le développement uniquement

ROOT_URLCONF = 'auto_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'auto_shop.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# auto_shop/settings.py

# Stripe
STRIPE_PUBLIC_KEY = 'pk_test_votre_cle_publique'
STRIPE_SECRET_KEY = 'sk_test_votre_cle_privee'
STRIPE_WEBHOOK_SECRET = 'whsec_votre_webhook_secret'

# Orange Money (Côte d'Ivoire)
ORANGE_MONEY_CLIENT_ID = 'votre_client_id'
ORANGE_MONEY_CLIENT_SECRET = 'votre_client_secret'
ORANGE_MONEY_MERCHANT_KEY = 'votre_merchant_key'
ORANGE_MONEY_API_URL = 'https://api.orange.com/orange-money/webpay/cm/v1/webpayment'

# MTN Mobile Money
MTN_MOMO_API_USER = 'votre_api_user'
MTN_MOMO_API_KEY = 'votre_api_key'
MTN_MOMO_SUBSCRIPTION_KEY = 'votre_subscription_key'
MTN_MOMO_API_URL = 'https://sandbox.momodeveloper.mtn.com'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# auto_shop/settings.py

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Pour Gmail (ou votre serveur SMTP)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'angeemmanuel2k06@gmail.com'  # Remplacez par votre email
EMAIL_HOST_PASSWORD = 'kjib zsfg yktu nmyr'  # Utilisez un mot de passe d'application
DEFAULT_FROM_EMAIL = 'AutoShop <angeemmanuel2k06@gmail.com>'
EMAIL_USE_SSL = False


# Configuration des messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Redirections après connexion/déconnexion
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'vehicle_list'
LOGOUT_REDIRECT_URL = 'vehicle_list'  # Important pour la redirection après déconnexion

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap5'