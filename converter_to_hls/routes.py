from views import status, start_convertation, check_state


def setup_routes(app):
    app.router.add_get('/status', status)
    app.router.add_post('/convert', start_convertation)

    # add server name in the url for scalability via load balancer
    #   the load balancer should be configured
    #   to redirect check_state request to proper converter's node by the 'server_name'
    app.router.add_get('/{server_name}/check_state/{task_id}', check_state)
    app.router.add_get('/check_state/{task_id}', check_state)
