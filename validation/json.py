from flask import request, jsonify
from functools import wraps
from voluptuous import MultipleInvalid, Invalid
from validation import schemas
from flask.json import loads as json_loads
from importlib import import_module


def validate_json(filename, schema_name):
    """
    Function for validating json requests.

    :attr
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            if not request.is_json:
                return jsonify(dict(message='Invalid type. Request data is not json')), 400

            mod = import_module('validation.schemas.' + filename)

            schema = getattr(mod, schema_name)

            try:
                schema(request.get_json())
            except MultipleInvalid as e:
                return jsonify(dict(message='Invalid data')), 400
            # except Invalid as e:
            #     return jsonify(dict(message='Invalid data')), 400

            return f(*args, **kw)
        return wrapper
    return decorator
