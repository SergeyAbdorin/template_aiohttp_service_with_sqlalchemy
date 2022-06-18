async def test_ready(app, aiohttp_client):
    cli = await aiohttp_client(app)
    resp = await cli.get('/healthz/ready')
    assert resp.status == 200
