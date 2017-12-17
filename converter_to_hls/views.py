from aiohttp import web
from aiohttp.web_exceptions import HTTPException, HTTPConflict, HTTPNotFound, HTTPInternalServerError

from hooks import validate_json
from schemas import LaunchConverterSchema
from services.transcoding import (
    LimitExceededException, DuplicatedTasksException, FailedToStartConvertation
)
from services.utils import build_state_link


async def status(request):
    if request.app['convert_manager'].limit_exceeded:
        return web.Response(status=509)
    return web.Response(status=200)


class HTTPLimitExceededException(HTTPException):
    status_code = 509


@validate_json(LaunchConverterSchema)
async def start_convertation(request):
    filename = (await request.json())['file']

    try:
        task = await request.app['convert_manager'].convert(filename)
    except LimitExceededException as e:
        raise HTTPLimitExceededException from e
    except DuplicatedTasksException as e:
        raise HTTPConflict from e
    except FileNotFoundError as e:
        raise HTTPNotFound from e
    except FailedToStartConvertation as e:
        raise HTTPInternalServerError from e

    check_state_link = build_state_link(task.task_id, request.app)
    return web.json_response(
        status=200,
        data={
            'task_id': task.task_id,
            'check_state': check_state_link,
            'file': filename,
        }
    )


async def check_state(request):
    task_id = request.match_info.get('task_id')
    try:
        converter = request.app['convert_manager'][task_id]
    except KeyError as e:
        raise HTTPNotFound from e
    return web.json_response(
        status=200,
        data={
            'task_id': task_id,
            'state': str(converter.state),
        }
    )
