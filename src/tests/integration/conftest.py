import pytest

from src.app.__main__ import prepare_app
from src.app.system import environment


@pytest.fixture
async def app(
    config,
):
    environment.initialize(config)
    _app = prepare_app(config)
    return _app
