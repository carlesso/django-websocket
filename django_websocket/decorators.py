from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import decorator_from_middleware
from django_websocket.middleware import BaseWebSocketMiddleware

__all__ = ('accept_websocket', 'require_websocket')


WEBSOCKET_MIDDLEWARE_INSTALLED = 'django_websocket.middleware.WebSocketMiddleware' in settings.MIDDLEWARE_CLASSES


def _setup_websocket(func):
    from functools import wraps
    @wraps(func)
    def new_func(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if response is None and request.is_websocket():
            return HttpResponse()
        return response
    if not WEBSOCKET_MIDDLEWARE_INSTALLED:
        decorator = decorator_from_middleware(BaseWebSocketMiddleware)
        new_func = decorator(new_func)
    return new_func


def accept_websocket(func):
    func = _setup_websocket(func)
    func.accept_websocket = True
    func.require_websocket = getattr(func, 'require_websocket', False)
    return func


def require_websocket(func):
    func = _setup_websocket(func)
    func.accept_websocket = True
    func.require_websocket = True
    return func