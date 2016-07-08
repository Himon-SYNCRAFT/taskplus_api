from voluptuous import All, Length, Schema, ALLOW_EXTRA, Required
from validation.utils import Coerce

login_min = 5
login_max = 128
first_name_min = 1
first_name_max = 128
last_name_min = 1
last_name_max = 128
password_min = 6
password_max = 128

update = Schema(
    {
        'login': All(str, Length(min=login_min, max=login_max)),
        'first_name': All(str, Length(min=first_name_min, max=first_name_max)),
        'last_name': All(str, Length(min=last_name_min, max=last_name_max)),
        'is_creator': bool,
        'is_contractor': bool,
        'is_admin': bool,
    },
    extra=ALLOW_EXTRA
)

create = Schema(
    {
        Required('login'): All(str, Length(min=login_min, max=login_max)),
        Required('first_name'): All(str, Length(min=first_name_min, max=first_name_max)),
        Required('last_name'): All(str, Length(min=last_name_min, max=last_name_max)),
        Required('password'): All(str, Length(min=password_min, max=password_max)),
        Required('is_creator'): bool,
        Required('is_contractor'): bool,
        Required('is_admin'): bool,
    },
    extra=ALLOW_EXTRA
)

query = Schema(
    {
        'id': Coerce(int),
        'login': All(str, Length(min=login_min, max=login_max)),
        'first_name': All(str, Length(min=first_name_min, max=first_name_max)),
        'last_name': All(str, Length(min=last_name_min, max=last_name_max)),
        'is_creator': Coerce(bool),
        'is_contractor': Coerce(bool),
        'is_admin': Coerce(bool),
    },
)
