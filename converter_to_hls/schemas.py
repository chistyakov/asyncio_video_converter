from marshmallow import Schema, fields


class LaunchConverterSchema(Schema):
    file = fields.Str(required=True, load_only=True)
