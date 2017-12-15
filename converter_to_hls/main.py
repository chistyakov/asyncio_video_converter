import os

from aiohttp import web

from middlwares import error_middleware
from routes import setup_routes


def create_app():
    app = web.Application(middlewares=[error_middleware,])
    setup_routes(app)
    app['host'] = os.environ.get('HOST', '0.0.0.0')
    app['port'] = int(os.environ.get('PORT', 8080))
    app['tasks'] = {}
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host=app['host'], port=app['port'])
