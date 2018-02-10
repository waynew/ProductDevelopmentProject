import json

from collections import OrderedDict

from flask.json import JSONEncoder
from . import db


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, db.RiskField):
                field = OrderedDict(
                    name=obj.type.name,
                    label=obj.label,
                    type=obj.type.type,
                )
                if obj.type.type == 'enum':
                    field['options'] = [json.loads(v.value) for v in obj.type.values]
                return field
            elif isinstance(obj, db.RiskType):
                type = OrderedDict(type=obj.name, label=obj.label, fields=obj.fields)
                return type
        except TypeError:
            pass
        return super().default(obj)

