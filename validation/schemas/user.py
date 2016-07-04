from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required

update = Schema(
    {
        'login': All(str, Length(min=1, max=128)),
        'first_name': All(str, Length(min=1, max=128)),
        'last_name': All(str, Length(min=1, max=128)),
        'is_creator': bool,
        'is_contractor': bool,
        'is_admin': bool,
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('login'): All(str, Length(min=1, max=128)),
        Required('first_name'): All(str, Length(min=1, max=128)),
        Required('last_name'): All(str, Length(min=1, max=128)),
        Required('password'): All(str, Length(min=6, max=128)),
        Required('is_creator'): bool,
        Required('is_contractor'): bool,
        Required('is_admin'): bool,
    },
    extra=ALLOW_EXTRA
)
