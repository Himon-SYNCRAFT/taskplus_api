from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required
from validation.utils import Coerce, ValueOperatorPair

value_min = 1

update = Schema(
    {
        'value': All(str, Length(min=value_min)),
        'task_id': int,
        'task_attribute_id': int,
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('value'): All(str, Length(min=value_min)),
        Required('task_id'): int,
        Required('task_attribute_id'): int,
    },
    extra=ALLOW_EXTRA
)

query = Schema(
    {
        'value': All(str, Length(min=value_min)),
        'task_id': Coerce(int),
        'task_attribute_id': Coerce(int),
    },
)

search = Schema(
    {
        'value': All(ValueOperatorPair(str), Length(min=value_min)),
        'task_id': ValueOperatorPair(int),
        'task_attribute_id': ValueOperatorPair(int),
    },
)
