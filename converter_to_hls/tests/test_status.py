async def test_hello(cli):
    resp = await cli.get('/status')
    assert resp.status == 200
