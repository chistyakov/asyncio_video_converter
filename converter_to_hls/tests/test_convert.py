from unittest import mock


async def test_launch_convert_success_response(cli):
    with mock.patch('views.build_state_link', return_value='link'), (
            mock.patch('views.build_task_id', return_value='uuid')
    ):
        resp = await cli.post('/convert', json={'file': 'small.mp4'})
        assert resp.status == 200
        data = await resp.json()
        assert data == {'task_id': 'uuid', 'check_state': 'link', 'file': 'small.mp4'}


async def test_launch_converter_bad_request(cli):
    resp = await cli.post('/convert', json={})
    assert resp.status == 400
    data = await resp.json()
    assert data == {'detail': {'file': ['Missing data for required field.']}}

    resp = await cli.post('/convert', data=b'foo')
    assert resp.status == 400


async def test_launch_converter_creates_task(cli):
    resp = await cli.post('/convert', json={'file': 'small.mp4'})
    assert resp.status == 200
    assert len(cli.server.app['tasks']) == 1
