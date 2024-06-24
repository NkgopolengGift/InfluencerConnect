# asgi.py

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import baseApplication.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InfluencerConnect.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            baseApplication.routing.websocket_urlpatterns
        )
    ),
})
