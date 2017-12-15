from functools import wraps
from json import JSONDecodeError

from aiohttp.web_exceptions import HTTPBadRequest


def validate_json(schema=None):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(request):
            data = await _extract_json(request)
            _validate_json_or_error(data, schema)
            return await handler(request)

        return wrapper

    return decorator


async def _extract_json(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise HTTPBadRequest(reason='expected json body')


def _validate_json_or_error(data, schema):
    if schema:
        errors = schema().validate(data)
        if errors:
            raise HTTPBadRequest(reason=errors)
