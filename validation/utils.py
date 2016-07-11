from voluptuous import Invalid
from datetime import datetime


def Coerce(type, msg=None):
    """Coerce a value to a type.

    If the type constructor throws a ValueError, the value will be marked as
    Invalid.
    """
    def f(v):
        try:
            return type(v)
        except ValueError:
            raise Invalid(msg or ('Expected %s' % type.__name__))
    return f


def ValueOperatorPair(type):
    def f(v):
        if not isinstance(v, dict):
            raise Invalid('expected dict')

        if 'operator' in v:
            operator = v['operator']
        else:
            operator = '='
        if 'value' not in v:
            raise Invalid("Expected dict which has 'value' key")
        value = v['value']

        try:
            return type(value)
        except ValueError:
            raise Invalid('Expected %s' % type.__name__)
    return f


def Date(fmt='%Y-%m-%dT%H:%M:%S.%f'):
    return lambda v: datetime.strptime(v, fmt)
    # YYYY-MM-DDTHH:MM:SS
