"""Twelve-factor configuration: values are read from environment variables."""
import os

from django.core.exceptions import ImproperlyConfigured


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=''):
    return [v.strip() for v in os.environ.get(name, default).split(',') if v.strip()]


DEBUG = env_bool('DJANGO_DEBUG', True)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if SECRET_KEY is None:
    if not DEBUG:
        raise ImproperlyConfigured('DJANGO_SECRET_KEY must be set when DEBUG is off')
    SECRET_KEY = 'django-insecure-dev-only-key'

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS')

if os.environ.get('DATABASE_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': os.environ['DATABASE_NAME'],
            'USER': os.environ.get('DATABASE_USER', ''),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
            'HOST': os.environ.get('DATABASE_HOST', ''),
            'PORT': os.environ.get('DATABASE_PORT', ''),
        }
    }

CORS_ALLOWED_ORIGINS = env_list('DJANGO_CORS_ALLOWED_ORIGINS', 'http://localhost:3000' if DEBUG else '')
CORS_ALLOW_CREDENTIALS = env_bool('DJANGO_CORS_ALLOW_CREDENTIALS', False)

# In dev, assets are served by the Rsbuild dev server; the manifest is still used
RSBUILD_BASE_URL = os.environ.get(
    'RSBUILD_BASE_URL', 'http://localhost:3000' if DEBUG else '/static'
)
