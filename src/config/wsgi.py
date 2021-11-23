"""
WSGI config for drfquickstart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(ROOT_DIR, "static"))
