from http import HTTPStatus

from aiohttp import web_request, web_response


async def get(request: web_request.Request) -> web_response.Response:
    """Сообщает о готовности сервиса к обработке запросов.

    ---
    get:
      tags:
        - Health checks
      description: Сообщает о готовности сервиса к обработке запросов.
      responses:
        '200':
          description: OK
        '503':
          description: UNREADY to accept requests
    """
    status = HTTPStatus.OK.value
    return web_response.Response(status=status)
