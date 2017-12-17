import logging

from aiohttp import web
from aiohttp.web_exceptions import HTTPException

from services.transcoding import ConverterException

logger = logging.getLogger(__name__)


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as ex:
        return json_error(ex)
    except Exception:
        logger.exception('Unhandled exception on %s %s', request.method, request.url)
        return web.json_response(status=500)


def json_error(ex):
    if ex.empty_body:
        return web.json_response(status=ex.status_code)
    data = {}
    cause_ex = ex.__cause__
    if isinstance(cause_ex, ConverterException):
        data['detail'] = str(cause_ex)
        if cause_ex.task_id:
            data['task_id'] = cause_ex.task_id
    elif isinstance(ex, HTTPException):
        data = {'detail': ex.reason}
    return web.json_response(status=ex.status_code, data=data)
