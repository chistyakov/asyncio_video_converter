import asyncio
import logging
import os
import socket

logger = logging.getLogger(__name__)


def build_state_link(task_id, app):
    api_url = build_base_api_url(app)
    return slash_safe_join_url(api_url, 'check_state', task_id)


def build_result_link(relative_output_path, app):
    if not relative_output_path:
        return None
    if app['config']['cdn_base_uri']:
        return slash_safe_join_url(app['config']['cdn_base_uri'], relative_output_path)
    else:
        return slash_safe_join_url(build_base_api_url(app), 'static', relative_output_path)


def build_base_api_url(app, append_server_name=True):
    uri = f'http://{app["config"]["host"]}:{app["config"]["port"]}'
    if append_server_name:
        uri = slash_safe_join_url(uri, get_server_name())
    return uri


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


async def makedirs(name, mode=0o777, loop=None, executor=None):
    loop = loop or asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor, os.makedirs, name, mode)
        return True
    except OSError:
        logger.exception('Error on creating the dir %s', name)
        return False


async def path_exists(path, loop=None, executor=None):
    loop = loop or asyncio.get_event_loop()
    return await loop.run_in_executor(executor, os.path.exists, path)
