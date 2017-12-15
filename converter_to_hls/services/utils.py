import socket
import uuid


def build_task_id():
    return str(uuid.uuid4())


def build_state_link(task_id, app):
    api_url = build_base_api_url(app)
    server_name = get_server_name()
    return slash_safe_join_url(api_url, server_name, 'check_state', task_id)


def build_base_api_url(app):
    return f'http://{app["host"]}:{app["port"]}'


def get_server_name():
    return socket.gethostname()


def slash_safe_join_url(*args):
    """
    >>> slash_safe_join_url('http://foo/', 'bar')
    'http://foo/bar'
    >>> slash_safe_join_url('http://foo/', '/bar')
    'http://foo/bar'
    >>> slash_safe_join_url('http://foo', '/bar')
    'http://foo/bar'
    >>> slash_safe_join_url('http://foo', 'bar')
    'http://foo/bar'
    >>> slash_safe_join_url('http://foo', 'bar', 'spam')
    'http://foo/bar/spam'
    >>> slash_safe_join_url('http://', 'server')  # BE CAREFUL
    'http:/server'
    >>> slash_safe_join_url('https://cdn/username/', 'servername', 'check_state', 'task_id')
    'https://cdn/username/servername/check_state/task_id'
    """
    return '/'.join(part.strip('/') for part in args)
