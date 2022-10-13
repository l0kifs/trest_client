import json


def is_json(value) -> bool:
    try:
        json.loads(value)
    except ValueError:
        return False
    return True
