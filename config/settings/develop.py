from decouple import config

from .base import *  # noqa: F403

SECRET_KEY = config('SECRET_KEY', default='dev-only-insecure-key-do-not-use-in-prod')

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}
