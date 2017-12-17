from views import status, start_convertation, check_state
from services.utils import get_server_name

def setup_routes(app):
    app.router.add_get('/status', status)
    app.router.add_post('/convert', start_convertation)

    # add server name in the url for scalability via load balancer
    #   the load balancer should be configured
    #   to redirect check_state request to proper converter's node by the 'server_name'
    server_name = get_server_name()
    app.router.add_get(f'/{server_name}/check_state/{{task_id}}', check_state)
    app.router.add_get('/check_state/{task_id}', check_state)

    # use nginx instead of the add_static
    app.router.add_static(f'/{server_name}/static', app['config']['output_dir'],
                          show_index=True)
    app.router.add_static('/static', app['config']['output_dir'], show_index=True)
