import re

from marshmallow import Schema, fields
from marshmallow.validate import Regexp

NO_SPECIAL_CHARS_PATTERN = re.compile('^[a-zA-Z0-9]+[a-zA-Z0-9_.\ -]*$')


class LaunchConverterSchema(Schema):
    file = fields.Str(
        required=True,
        load_only=True,
        validate=Regexp(NO_SPECIAL_CHARS_PATTERN, error='Invalid filename.')
    )
