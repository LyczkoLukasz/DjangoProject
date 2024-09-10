import os
import django

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from notifications.routing import websocket_urlpatterns

from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django_asgi_app = get_asgi_application()
django.setup()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
