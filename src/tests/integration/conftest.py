import pytest

from app.service import prepare_app
from app.system import environment


@pytest.fixture
async def app(
    config,
):
    environment.initialize(config)
    _app = prepare_app(config)
    return _app
