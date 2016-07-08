from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required
from validation.utils import Coerce


update = Schema(
    {
        'task_type_id': int,
        'task_attribute_id': int,
        'sort': int,
        'rules': str
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('task_type_id'): int,
        Required('task_attribute_id'): int,
        'sort': int,
        'rules': str
    },
    extra=ALLOW_EXTRA
)

query = Schema(
    {
        'task_type_id': Coerce(int),
        'task_attribute_id': Coerce(int),
        'sort': Coerce(int),
        'rules': str
    },
)
