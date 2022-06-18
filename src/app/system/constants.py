from enum import Enum, auto, unique


@unique
class App(Enum):
    """Содержит ключи к объектам в web.Application."""

    config = auto()
    trump_cli = auto()
    trace_config = auto()
    http_cli = auto()
    db_conn = auto()
