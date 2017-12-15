from aiohttp import web


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as ex:
        return json_error(ex)
    except Exception:
        return web.json_response(status=500)


def json_error(ex):
    if ex.empty_body:
        return web.json_response(status=ex.status_code)
    return web.json_response(status=ex.status_code, data={'detail': ex.reason})
