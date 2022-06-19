import logging
import os

import asyncpg
from aiohttp import web
from aiohttp.client import ClientSession, ClientTimeout
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import select

from src.app.system import environment
from src.app.system.constants import App

load_dotenv()


async def _setup_client_session(app: web.Application):
    """Настройка http клиента."""
    cli = ClientSession(
        timeout=ClientTimeout(total=app[App.config.name]['client']['timeout']),
    )
    app[App.http_cli.name] = cli
    yield
    await cli.close()


async def _setup_db_connection(app: web.Application):
    """Настройка подключения к базе данных.

    Безопасно завершает подключение после остановки приложения.

    Yields:
        connect to db.
    """
    logging.info('Connecting to database')
    app[App.db_conn.name] = create_async_engine(
        environment.get_db_url(is_async=True)
    )
    async with app[App.db_conn.name].begin() as conn:
        await conn.execute(select(1))

    logging.info('Connected to database')

    try:
        yield
    finally:
        logging.info('Disconnecting from database')
        await app[App.db_conn.name].dispose()
        logging.info('Disconnected from database')


def setup_connections(app: web.Application):
    """Дополняет подключения при старте приложения.

    :param app: экземпляр приложения
    """
    app.cleanup_ctx.extend((
        _setup_client_session,
        _setup_db_connection,
    ))
