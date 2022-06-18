import argparse
import logging
import os
import pathlib
import sys

from aiohttp import web
from aiohttp_swagger import setup_swagger

from app.api.routes import setup_routes
from app.system.constants import App
from app.system import environment
from app.system.middlewares import setup_middlewares
from app.system.settings import setup_connections


def prepare_app(config):
    """Настраивает экземпляр aiohttp.Application.

    :return: настроенный экземпляр aiohttp.Application
    """
    app = web.Application()
    app[App.config.name] = config
    setup_routes(app)
    setup_middlewares(app)
    setup_connections(app)

    project_root = pathlib.Path(__file__).parent.parent.parent.resolve()
    path_to_swagger_file = os.path.join(
        project_root,
        'public',
        'docs',
        f'v{config["service"]["version"]}',
        'swagger.yml',
    )
    setup_swagger(
        app,
        ui_version=3,
        swagger_from_file=path_to_swagger_file,
    )

    return app


def start():
    """Запускает сервис."""
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '-c',
        '--config',
        type=str,
        required=True,
        help='Path to configuration file',
    )
    ap.add_argument(
        '--env_prefix',
        type=str,
        help='Prefix for environment variables',
    )

    options, _ = ap.parse_known_args(sys.argv[1:])
    config = environment.get_config(options)

    environment.initialize(config)
    logging.info(config)

    web.run_app(
        prepare_app(config),
        port=config['service']['port'],
        access_log=None,
    )


if __name__ == '__main__':
    start()
