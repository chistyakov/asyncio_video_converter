from unittest.mock import Mock

import pytest

from services.transcoding import State
from unittest.mock import patch


# TODO: move to unit test for the build_result_link
@pytest.mark.parametrize(
    'config_diff,result_uri',
    [
        ({'cdn_base_uri': 'http://cdn.com'}, 'http://cdn.com/uuid/playlist.m3u8'),
        ({'host': 'localhost', 'port': '80'}, 'http://localhost:80/hostname/static/uuid/playlist.m3u8'),
    ])
async def test_check_state_success_response(cli, config_diff, result_uri):
    with patch('socket.gethostname', return_value='hostname'):
        cli.server.app['convert_manager'].tasks = {
            'uuid': Mock(task_id='uuid', state=State.FINISHED_SUCCESSFULLY,
                         relative_output_path='uuid/playlist.m3u8')
        }
        cli.server.app['config'] = dict(cli.server.app['config'])
        cli.server.app['config'].update(config_diff)

        resp = await cli.get('/check_state/uuid')
        assert resp.status == 200
        assert await resp.json() == {
            'task_id': 'uuid',
            'state': 'finished_successfully',
            'result': result_uri
        }


async def test_check_state_of_non_existing_task(cli):
    resp = await cli.get('/check_state/uuid')
    assert resp.status == 404
