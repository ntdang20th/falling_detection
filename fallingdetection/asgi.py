"""
ASGI config for fallingdetection project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os


from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from api.consumers import SensorConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fallingdetection.settings')
application = get_asgi_application()
ws_patterns = [
    path('ws/sensor/', SensorConsumer.as_asgi()),
]
application = ProtocolTypeRouter({
    'websocket': URLRouter(ws_patterns)
})
