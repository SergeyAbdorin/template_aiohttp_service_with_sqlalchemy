import logging
import os

import asyncpg
from aiohttp import web
from aiohttp.client import ClientSession, ClientTimeout
from dotenv import load_dotenv

from app.system.constants import App

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
    """Настройка подключения к базе данных."""
    logging.info('Connecting to database')
    conn = await asyncpg.connect(
        user=os.environ.get('DB_USR'),
        password=os.environ.get('DB_PWD'),
        database=os.environ.get('DB_NM'),
        host=os.environ.get('DB_HST'),
        port=os.environ.get('DB_PRT'),
    )
    app[App.db_conn.name] = conn
    await conn.fetch('SELECT 1')
    logging.info('Connected to database')

    yield

    logging.info('Disconnecting from database')
    await conn.close()
    logging.info('Disconnected from database')


def setup_connections(app: web.Application):
    """Дополняет подключения при старте приложения.

    :param app: экземпляр приложения
    """
    app.cleanup_ctx.extend((
        _setup_client_session,
        _setup_db_connection,
    ))
