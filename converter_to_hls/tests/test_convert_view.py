from unittest.mock import patch, Mock

import pytest
from asynctest.mock import patch as async_patch

from services.transcoding import State


async def test_run_convert_success_response(cli):
    with patch('views.build_state_link', return_value='link'), (
            patch('services.transcoding.manager.ConvertTask.build_task_id', return_value='uuid')), (
                 async_patch('services.transcoding.manager.ConvertTask.run')):
        resp = await cli.post('/convert', json={'file': 'foo.mp4'})
        assert resp.status == 200
        resp_data = await resp.json()
        assert resp_data == {'task_id': 'uuid', 'check_state': 'link', 'file': 'foo.mp4'}


async def test_run_converter_with_invalid_filename(cli):
    resp = await cli.post('/convert', json={})
    assert resp.status == 400
    resp_data = await resp.json()
    assert resp_data == {'detail': {'file': ['Missing data for required field.']}}

    resp = await cli.post('/convert', data=b'foo')
    assert resp.status == 400


async def test_run_convert_creates_task(cli):
    with async_patch('services.transcoding.manager.ConvertTask.run') as patched_run:
        resp = await cli.post('/convert', json={'file': 'foo.mp4'})
        assert resp.status == 200
        patched_run.assert_called_once()
    assert len(cli.server.app['convert_manager']) == 1


async def test_converts_limit_exceeded(cli):
    cli.server.app['convert_manager'].tasks = {
        'uuid1': Mock(task_id='uuid', state=State.RUNNING),
        'uuid2': Mock(task_id='uuid', state=State.RUNNING),
        'uuid3': Mock(task_id='uuid', state=State.RUNNING),
        'uuid4': Mock(task_id='uuid', state=State.RUNNING),
        'uuid5': Mock(task_id='uuid', state=State.RUNNING),
    }
    with async_patch('services.transcoding.manager.ConvertTask.run'):
        resp = await cli.post('/convert', json={'file': 'foo.mp4'})
        assert resp.status == 509
        assert await resp.json() == {'detail': 'Running tasks limit exceeded. Limit: 5.'}


async def test_task_id_collision(cli):
    with async_patch('services.transcoding.manager.ConvertTask.run'), (
            patch('services.transcoding.manager.ConvertTask.build_task_id', return_value='foo')
    ):
        resp = await cli.post('/convert', json={'file': 'foo.mp4'})
        assert resp.status == 200
        resp = await cli.post('/convert', json={'file': 'foo.mp4'})
        assert resp.status == 409
        assert await resp.json() == {'detail': 'Task already exists. Task id: foo.', 'task_id': 'foo'}


async def test_run_convert_for_not_existing_file(cli):
    resp = await cli.post('/convert', json={'file': 'foo.mp4'})
    assert resp.status == 404


@pytest.mark.parametrize('filename', ['../../foo.mp4', '/root/', '.', '..', '.gitignore'])
async def test_run_convert_with_dangerous_filename(cli, filename):
    resp = await cli.post('/convert', json={'file': filename})
    assert resp.status == 400
    assert await resp.json() == {'detail': {'file': ['Invalid filename.']}}


async def test_error_on_start_ffmpeg(cli):
    with patch('os.path.exists', return_value=True), patch('os.makedirs'), (
            async_patch('asyncio.create_subprocess_exec', side_effect=OSError)), (
                 patch('services.transcoding.manager.ConvertTask.build_task_id', return_value='foo')):
        resp = await cli.post('/convert', json={'file': 'foo.mp4'})
        assert resp.status == 500
        assert await resp.json() == {'detail': 'Failed to start convertation.', 'task_id': 'foo'}
