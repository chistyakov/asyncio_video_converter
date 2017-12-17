async def test_status(cli):
    resp = await cli.get('/status')
    assert resp.status == 200
