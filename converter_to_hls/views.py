from aiohttp import web


async def status(request):
    return web.Response(status=200)
