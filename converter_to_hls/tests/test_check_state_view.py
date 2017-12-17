from unittest.mock import Mock

from services.transcoding import State


async def test_check_state_success_response(cli):
    cli.server.app['convert_manager'].tasks = {
        'uuid': Mock(task_id='uuid', state=State.FINISHED_SUCCESSFULLY)
    }
    resp = await cli.get('/check_state/uuid')
    assert resp.status == 200
    assert await resp.json() == {'task_id': 'uuid', 'state': 'finished_successfully'}


async def test_check_state_of_non_existing_task(cli):
    resp = await cli.get('/check_state/uuid')
    assert resp.status == 404
