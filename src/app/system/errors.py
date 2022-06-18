from http import HTTPStatus
from typing import Any, Dict

UNEXPECTED_ERROR = 1
FILE_NOT_UPLOADED = 2
FILE_TYPE_NOT_SUPPORTED = 3
CANNOT_PROCESS_IMAGE = 4
UNKNOWN_DOCUMENT_TYPE = 5
INVALID_JSON = 6
NOT_ALL_ARGUMENTS_PROVIDED = 7
INVALID_REQUEST = 8


class ServiceError(Exception):
    """Базовый класс для ошибок приложения."""

    def __init__(
        self,
        message: str = 'Unexpected error',
        http_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        code: int = UNEXPECTED_ERROR,
    ):
        """Создает экземпляр Service Error.

        :param message: сообщение ошибки
        :param http_code: http код ошибки
        :param code: код ошибки приложения
        """
        super().__init__(message)
        self.code = code
        self.http_code = http_code
        self.message = message

    def as_json_obj(self) -> Dict[str, Any]:
        """Получить json представление объекта ошибки.

        :return: сообщение в формате JSON
        """
        return {'code': self.code, 'http_status': self.http_code, 'message': self.message}


class InvalidRequestError(ServiceError):
    """Базовый класс для ошибок связанных с некорректными входными запросами."""

    def __init__(  # noqa: WPS612
        self,
        message: str = 'Invalid request',
        http_code: int = HTTPStatus.BAD_REQUEST,
        code: int = INVALID_REQUEST,
    ):
        """Создает экземпляр Invalid Request Error с соответствующим сообщением по умолчанию.

        :param message: сообщение ошибки
        :param http_code: http код ошибки
        :param code: код ошибки приложения
        """
        super().__init__(message, http_code, code)
