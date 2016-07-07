from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required

value_min = 1
name_max = 128

update = Schema(
    {
        'value': All(str, Length(min=value_min)),
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('value'): All(str, Length(min=value_min)),
    },
    extra=ALLOW_EXTRA
)

query = Schema(
    {
        'value': All(str, Length(min=value_min)),
    },
)
