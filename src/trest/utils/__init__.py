import json


def is_json_string(value: str) -> bool:
    try:
        json.loads(value)
    except ValueError:
        return False
    return True
