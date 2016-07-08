from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required
from validation.utils import Coerce, ValueOperatorPair

name_min = 1
name_max = 128

update = Schema(
    {
        'name': All(str, Length(min=name_min, max=name_max)),
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('name'): All(str, Length(min=name_min, max=name_max)),
    },
    extra=ALLOW_EXTRA
)

query = Schema(
    {
        'name': All(str, Length(min=name_min, max=name_max)),
        'id': Coerce(int)
    },
)

search = Schema(
    {
        'name': All(ValueOperatorPair(str), Length(min=name_min, max=name_max)),
        'id': ValueOperatorPair(int)
    },
)
