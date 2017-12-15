from aiohttp import web

from hooks import validate_json
from schemas import LaunchConverterSchema
from services.utils import build_task_id, build_state_link


async def status(request):
    return web.Response(status=200)


@validate_json(LaunchConverterSchema)
async def start_convertation(request):
    task_id = build_task_id()
    check_state_link = build_state_link(task_id, request.app)
    data = await request.json()
    filename = data['file']
    request.app['tasks'][task_id] = None
    return web.json_response(
        status=200,
        data={
            'task_id': task_id,
            'check_state': check_state_link,
            'file': filename,
        }
    )
