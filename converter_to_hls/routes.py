from views import status, start_convertation


def setup_routes(app):
    app.router.add_get('/status', status)
    app.router.add_post('/convert', start_convertation)
