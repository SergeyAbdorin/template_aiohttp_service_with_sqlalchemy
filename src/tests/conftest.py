import os
import pathlib
import pytest
import yaml


BASE_DIR = pathlib.Path(__file__).parent.parent
path_to_config_file = os.path.join(BASE_DIR, 'config/default.yaml')


@pytest.fixture(scope='session')
def config():
    """Конфигурация сервиса в виде dict."""
    config = yaml.safe_load(pathlib.Path(path_to_config_file).read_text())
    config['logging']['root']['handlers'] = ['console']
    return config
