import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chessapp.routing import websocket_urlpatterns  # Import your routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chess-Sid.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Make sure this is correctly configured
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})