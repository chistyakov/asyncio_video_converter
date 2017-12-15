from views import status


def setup_routes(app):
    app.router.add_get('/status', status)
