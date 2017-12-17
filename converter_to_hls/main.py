import asyncio
import logging
import os
from types import MappingProxyType

from aiohttp import web

from middlwares import error_middleware
from routes import setup_routes
from services.transcoding import ConvertManager

logging.basicConfig(level=logging.DEBUG)


def create_app(loop):
    app = web.Application(middlewares=[error_middleware, ])
    setup_routes(app)
    app['config'] = MappingProxyType(
        {
            'host': os.environ.get('HOST', '0.0.0.0'),
            'port': int(os.environ.get('PORT', 8080)),
            'tasks_limit': int(os.environ.get('TASKS_LIMIT', 5)),
            'output_dir': os.environ.get('OUTPUT_DIR', '/output'),
            'input_dir': os.environ.get('INPUT_DIR', '/input'),
        }
    )
    # TODO: add bootstrapping of the ConvertManager from filesystem on app's initialization
    #       (add existing m3u8 files with the finalization string '#EXT-X-ENDLIST' to tasks registry)
    #       to come through application's restart
    app['convert_manager'] = ConvertManager(app['config'], loop)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = create_app(loop)
    web.run_app(app, host=app['config']['host'], port=app['config']['port'], loop=loop)
