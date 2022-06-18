import argparse
import os
import pathlib
import shutil
import sys
import yaml

from aiohttp.web import Application

from app.api.routes import setup_routes
from app.system import environment
from tools.apispec.plugin import ApiDocsGenerator

if __name__ == '__main__':
    BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
    path_to_config_file = os.path.join(BASE_DIR, 'src/config/default.yaml')
    config = yaml.safe_load(pathlib.Path(path_to_config_file).read_text())

    application_version = config['service']['version']
    spec_path: pathlib.Path = BASE_DIR / 'public' / 'docs' / f'v{application_version}'

    if os.path.exists(spec_path):
        raise FileExistsError('Данная версия АПИ уже существует')

    app = Application()
    app['static_dir'] = 'app/swagger'
    setup_routes(app)

    service_name = config['service']['name']
    OPENAPI_SPEC = f"""
        openapi: 3.0.2
        info:
          description: {service_name} service API
          title: {service_name} service API

          version: {application_version}
        servers:
        - url: http://localhost:{config['service']['port']}/
          description: The local API server
        """

    docs_generator = ApiDocsGenerator(app, openapi_base=OPENAPI_SPEC)

    yaml_spec = docs_generator.generate()
    spec_path.mkdir(parents=True, exist_ok=True)
    with (spec_path / 'swagger.yml').open('w', encoding='utf-8') as api_file:
        api_file.write(yaml_spec)
    shutil.copyfile(
        BASE_DIR / 'tools' / 'apispec' / 'api_view.html', spec_path / 'api_view.html',
    )
