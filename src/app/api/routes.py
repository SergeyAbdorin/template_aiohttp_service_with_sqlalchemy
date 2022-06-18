import aiohttp_cors
from aiohttp import web

from app.api.healthz import ready


def setup_routes(app: web.Application):
    """Инициализирует маршруты приложения."""
    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        ),
    })

    # Служебные эндпоинты
    cors.add(app.router.add_get('/healthz/ready', ready.get))
