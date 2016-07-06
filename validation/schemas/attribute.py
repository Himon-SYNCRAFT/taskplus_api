from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required

name_min = 1
name_max = 128

update = Schema(
    {
        'name': All(str, Length(min=name_min, max=name_max)),
        'type_id': int,
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('name'): All(str, Length(min=name_min, max=name_max)),
        Required('type_id'): int,
    },
    extra=ALLOW_EXTRA
)

query = Schema(
    {
        'name': All(str, Length(min=name_min, max=name_max)),
        'type_id': int,
    },
)
