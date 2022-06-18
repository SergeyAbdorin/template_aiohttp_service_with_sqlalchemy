import apispec
import apispec.yaml_utils
import yaml
from apispec.ext.marshmallow import MarshmallowPlugin


class UnicodeFriendlyAPISpec(apispec.APISpec):
    """Класс для генерации документации по API."""

    def to_yaml(self):
        """Перевод в YAML-формат.

        :return: Содержимое в YAML-формате
        """
        return yaml.dump(
            self.to_dict(),
            Dumper=apispec.yaml_utils.YAMLDumper,
            allow_unicode=True,
        )


class ApiDocsGenerator:
    """Автоматически генерирует документацию по API на основе aiohttp.web.Application."""

    app = None
    spec: apispec.APISpec = None

    def __init__(self, application, openapi_base: str, plugins: tuple = (MarshmallowPlugin(),)):
        """Конструктор генератора документации по API на основе aiohttp.web.Application.

        :param application: Инстанс aiohttp-приложения с установленными маршрутами
        :param openapi_base: Описание базы для OpenAPI документации
        :param plugins: Кортеж плагинов для генерации OpenAPI документации
        """
        ApiDocsGenerator.app = application

        settings = ApiDocsGenerator._parse_openapi_base(openapi_base)

        ApiDocsGenerator.spec = UnicodeFriendlyAPISpec(
            title=settings['info']['title'],
            version=settings['info']['version'],
            openapi_version=settings['openapi'],
            plugins=plugins,
            **settings,
        )

    @classmethod
    def _parse_openapi_base(cls, openapi_base: str) -> dict:
        return yaml.safe_load(openapi_base)

    def _register_route(self, route) -> None:
        self.spec.path(
            path=route.resource.canonical,
            operations=apispec.yaml_utils.load_operations_from_docstring(route.handler.__doc__),
        )

    def generate(self) -> str:
        """Generate."""
        for route in self.app.router.routes():
            self._register_route(route)
        return self.spec.to_yaml()
