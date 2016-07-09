from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required
from validation.utils import Coerce, ValueOperatorPair, Date

name_min = 1
name_max = 128

update = Schema(
    {
        'name': All(str, Length(min=name_min, max=name_max)),
        'external_identifier': All(str, Length(min=name_min, max=name_max)),
        'type_id': int,
        'end_date': All(Date(), Length(min=name_min, max=name_max)),
        'create_date': All(Date(), Length(min=name_min, max=name_max)),
        'status_id': int,
        'creator_id': int,
        'contractor_id': int,
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('name'): All(str, Length(min=name_min, max=name_max)),
        'external_identifier': All(str, Length(min=name_min, max=name_max)),
        Required('type_id'): int,
        'end_date': All(Date(), Length(min=name_min, max=name_max)),
        'create_date': All(Date(), Length(min=name_min, max=name_max)),
        Required('status_id'): int,
        Required('creator_id'): int,
        'contractor_id': int,
    },
    extra=ALLOW_EXTRA
)

query = Schema(
    {
        'id': Coerce(int),
        'name': All(str, Length(min=name_min, max=name_max)),
        'external_identifier': All(str, Length(min=name_min, max=name_max)),
        'type_id': Coerce(int),
        'end_date': All(Date(), Length(min=name_min, max=name_max)),
        'create_date': All(Date(), Length(min=name_min, max=name_max)),
        'status_id': Coerce(int),
        'creator_id': Coerce(int),
        'contractor_id': Coerce(int),
    },
)

search = Schema(
    {
        'id': ValueOperatorPair(int),
        'name': All(ValueOperatorPair(str), Length(min=name_min, max=name_max)),
        'external_identifier': All(ValueOperatorPair(str), Length(min=name_min, max=name_max)),
        'type_id': ValueOperatorPair(int),
        'end_date': All(ValueOperatorPair(Date()), Length(min=name_min, max=name_max)),
        'create_date': All(ValueOperatorPair(Date()), Length(min=name_min, max=name_max)),
        'status_id': ValueOperatorPair(int),
        'creator_id': ValueOperatorPair(int),
        'contractor_id': ValueOperatorPair(int),
    },
)
