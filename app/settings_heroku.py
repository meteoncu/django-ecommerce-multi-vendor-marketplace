from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = [
    "emte-ecommerce.herokuapp.com",
    "127.0.0.1",
    "*",
]

MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

DEBUG = True
