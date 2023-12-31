"""
WSGI config for OrderManager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .settings import base_settings

# set postgres as the default database
os.environ.setdefault('DB_TYPE', 'postgres')

# Based on the DEBUG flag, the application will automatically switch between local and prod settings
if base_settings.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderManager.settings.local_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderManager.settings.prod_settings')


application = get_wsgi_application()
