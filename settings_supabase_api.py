import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Detecta produção
PRODUCTION = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PRODUCTION', 'False').lower() == 'true'

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-6c!7%^w=v&0++twoi_5d0g5jdy5xvr)35v#dqn7wp#u%j6^3i#')
DEBUG = not PRODUCTION

ALLOWED_HOSTS = ['.railway.app', '.up.railway.app', 'localhost', '127.0.0.1', '0.0.0.0'] if PRODUCTION else ['localhost', '127.0.0.1', '0.0.0.0']

# Configurações do Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://zyeaqpsltgavouygatxs.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5ZWFxcHNsdGdhdm91eWdhdHhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4MjQ4NDMsImV4cCI6MjA2MzQwMDg0M30.L9SVkjKQk2cVygHIIcjC0T9YQ_SEZXRUvSSMOYhDWvE')

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

if PRODUCTION:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    INSTALLED_APPS.insert(-1, 'whitenoise.runserver_nostatic')

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

# Database - SQLite para Django, Supabase REST API para dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuração especial para produção
if PRODUCTION:
    # Em produção, usar SQLite em memória para Django (apenas sessões, admin)
    DATABASES['default']['NAME'] = ':memory:'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'painel_usuario'

# Configuração customizada para usar Supabase
AUTH_USER_MODEL = 'auth.User'  # Usar User padrão do Django

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if PRODUCTION:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if PRODUCTION:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'supabase': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

