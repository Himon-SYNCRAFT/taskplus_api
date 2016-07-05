from flask import request, jsonify
from functools import wraps
from voluptuous import MultipleInvalid, Invalid
from validation import schemas
from flask.json import loads as json_loads
from importlib import import_module


def validate_query(filename, schema_name):
    """
    Decorator for validating requests.args.

    Function uses schema 'schema_name' which can be find in
    '/validation/schemas/filename.py'
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            mod = import_module('validation.schemas.' + filename)
            schema = getattr(mod, schema_name)

            try:
                schema(request.args.to_dict())
            except MultipleInvalid as e:
                message = 'Invalid value for {0}. {1}'.format(
                    e.path, e.error_message)
                return jsonify(dict(message=message)), 400

            return f(*args, **kw)
        return wrapper
    return decorator
