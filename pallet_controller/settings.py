import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Detecta se está em produção (Railway ou outras plataformas)
PRODUCTION = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PRODUCTION', False)

if PRODUCTION:
    # Carrega configurações de produção
    from .settings_production import *
else:
    # Configurações de desenvolvimento

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-6c!7%^w=v&0++twoi_5d0g5jdy5xvr)35v#dqn7wp#u%j6^3i#'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

    # Configurações do Supabase
    SUPABASE_URL = 'https://zyeaqpsltgavouygatxs.supabase.co'
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5ZWFxcHNsdGdhdm91eWdhdHhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4MjQ4NDMsImV4cCI6MjA2MzQwMDg0M30.L9SVkjKQk2cVygHIIcjC0T9YQ_SEZXRUvSSMOYhDWvE'

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'app_controller',
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

    ROOT_URLCONF = 'pallet_controller.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

    WSGI_APPLICATION = 'pallet_controller.wsgi.application'

    # Database - Desenvolvimento com Supabase
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': '5IEvXIKjw9BN2QOx',
            'HOST': 'db.zyeaqpsltgavouygatxs.supabase.co',
            'PORT': '5432',
        }
    }

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
    ]

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

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    ]

    LOGIN_URL = 'login'
    LOGIN_REDIRECT_URL = 'painel_usuario'
    AUTH_USER_MODEL = 'app_controller.Usuario'

    LANGUAGE_CODE = 'pt-br'
    TIME_ZONE = 'America/Sao_Paulo'
    USE_I18N = True
    USE_TZ = True

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Default primary key field type
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'