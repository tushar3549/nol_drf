from .base import *

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Whitenoise static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
