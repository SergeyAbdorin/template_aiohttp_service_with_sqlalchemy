import os
import yaml

from logging import config
from pathlib import Path


def _configure_logging(log_config):
    """Настраивает формат логирования в соответствии с конфигурацией.

    :param log_config: конфигурация логера
    """

    config.dictConfig(log_config)


def initialize(common_config):
    """Инициализирует все обертки над либами для Application.

    :param common_config: конфигурация приложения
    """

    _configure_logging(common_config['logging'])


def get_config(options):
    """Возвращает конфигурацию приложения."""
    try:
        config = yaml.safe_load(Path(options.config).read_text())
    except FileNotFoundError:
        path_to_dir = Path(__file__).parent.parent.parent.parent
        options.config = os.path.join(path_to_dir, options.config)
        config = yaml.safe_load(Path(options.config).read_text())
    return config


def get_db_url(is_async: bool = False):
    """Возвращает url для подключения к базе данных."""
    if is_async:
        prefix = 'postgresql+asyncpg'
    else:
        prefix = 'postgresql'

    return (
        f'{prefix}://{os.environ.get("DB_USR")}'
        f':{os.environ.get("DB_PWD")}'
        f'@{os.environ.get("DB_HST")}'
        f':{os.environ.get("DB_PRT")}'
        f'/{os.environ.get("DB_NM")}'
    )