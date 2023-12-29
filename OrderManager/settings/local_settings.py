from .base_settings import *

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'OrderManager/local_db.sqlite3',
    }
}

# Based on the DEBUG flag, the application will automatically switch between local and prod settings
# The logic can be found within the manange.py file