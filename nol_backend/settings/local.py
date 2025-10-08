from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-m8cund7g7=81$ub0yi=e32^#l6r$yjk@qf7@_4)*h7a5r#mu)8'
ALLOWED_HOSTS = ['*']



#database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')