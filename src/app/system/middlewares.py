import logging
import time
from http import HTTPStatus
from typing import Awaitable, Callable
from uuid import uuid4

from aiohttp import web, web_exceptions, web_middlewares
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse
from opentracing import global_tracer, propagation, tags

from src.app.system import errors

RequestHandler = Callable[[Request], Awaitable[StreamResponse]]
MiddlewareFunction = Callable[[Request, RequestHandler], Awaitable[StreamResponse]]

_ENDPOINT = 'endpoint'


@web_middlewares.middleware
async def _common_middleware(request: Request, handler: RequestHandler) -> StreamResponse:
    """Подготавливает запрос к обработке и логирует результат.

    :param request: пришедший в сервис запрос
    :param handler: обработчик запроса
    :return: результат обработки запроса
    """
    request['start_time'] = time.time()
    request[_ENDPOINT] = f'{request.method} {request.path}'

    response = await handler(request)

    logging.info({
        'time': time.time() - request['start_time'],
        'status_code': response.status,
        _ENDPOINT: request[_ENDPOINT],
    })
    return response


@web_middlewares.middleware
async def _errors_middleware(request: Request, handler: RequestHandler) -> StreamResponse:
    """Middleware для обработки ошибок.

    :param request: пришедший в сервис запрос
    :param handler: обработчик запроса
    :return: результат обработки запроса
    """
    try:
        return await handler(request)
    except web_exceptions.HTTPException as http_err:
        logging.exception({'error': http_err.reason})
        return web.json_response(
            {'error': http_err.reason},
            status=http_err.status,
        )
    except errors.ServiceError as service_err:
        logging.exception({'error': str(service_err)})
        return web.json_response(
            {'error': str(service_err)},
            status=service_err.http_code,
        )
    except Exception:
        error_text = 'Serious unexpected error'
        logging.exception(error_text)
        return web.json_response(
            {'error': error_text},
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@web_middlewares.middleware
async def _tracing_middleware(request: Request, handler: RequestHandler) -> StreamResponse:
    """Middleware для реализации трейсинга.

    Извлекает из хедеров информацию о трейсинге и создает корневой спан на запрос.
    :param request: пришедший в сервис запрос
    :param handler: обработчик запроса
    :return: результат обработки запроса
    """
    span_ctx = global_tracer().extract(propagation.Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: request.path,
    }
    with global_tracer().start_active_span(request.path, child_of=span_ctx, tags=span_tags):
        return await handler(request)


def setup_middlewares(app: web.Application):
    """Дополняет стандартные middleware кастомными.

    :param app: экземпляр приложения
    """
    app.middlewares.extend((
        _common_middleware,
        _errors_middleware,
        _tracing_middleware,
    ))
