from typing import List

from aiohttp import web
from aiohttp_cors import CorsViewMixin

from src.app.system.constants import App


class BaseView(web.View, CorsViewMixin):
    """Базовый класс обработчиков."""

    url_path: List[str]

    @property
    def pg(self):
        """Подключение к базе данных."""
        return self.request.app[App.db_conn.name]
