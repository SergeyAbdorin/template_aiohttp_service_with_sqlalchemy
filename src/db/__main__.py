import argparse
import logging
import os
import sys
from pathlib import Path

from alembic.config import CommandLine, Config
from dotenv import load_dotenv

from src.app.system import environment


PROJECT_PATH = Path(__file__).parent.parent.resolve()
load_dotenv()


def make_alembic_config(cmd_opts, base_path: str = PROJECT_PATH) -> Config:
    """Конфигурация alembic.

    Создает объект конфигурации alembic на основе аргументов командной строки,
    подменяет относительные пути на абсолютные.
    """
    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            'script_location',
            os.path.join(base_path, alembic_location),
        )
    if cmd_opts.db_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.db_url)

    return config


def main():
    """Утилита для управления состоянием базы данных, обертка над alembic.

    Можно вызывать из любой директории, а также указать произвольный DSN для базы
    данных, отличный от указанного в файле alembic.ini.
    """
    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    options = alembic.parser.parse_args()
    ap = argparse.ArgumentParser()

    options_app, _ = ap.parse_known_args(sys.argv[1:])

    options.db_url = environment.get_db_url(is_async=False)

    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
        exit_var = 128
        exit(exit_var)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
