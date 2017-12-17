import asyncio
import logging
import os
import socket

logger = logging.getLogger(__name__)


def build_state_link(task_id, app):
    api_url = build_base_api_url(app)
    server_name = get_server_name()
    return slash_safe_join_url(api_url, server_name, 'check_state', task_id)


def build_base_api_url(app):
    return f'http://{app["config"]["host"]}:{app["config"]["port"]}'


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


async def makedirs(name, mode=0o777, loop=None):
    loop = loop or asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, os.makedirs, name, mode)
        return True
    except OSError:
        logger.exception('Error on creating the dir %s', name)
        return False


async def path_exists(path, loop=None):
    loop = loop or asyncio.get_event_loop()
    return await loop.run_in_executor(None, os.path.exists, path)
