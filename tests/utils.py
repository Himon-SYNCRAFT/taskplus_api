from json.decoder import JSONDecodeError
from flask.json import loads as json_loads

def is_json(data):
    try:
        json_loads(data)
    except JSONDecodeError:
        return False
    return True
