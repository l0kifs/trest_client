import inspect
import json
import logging
from dataclasses import is_dataclass
from typing import Any

from jto import JTOConverter

from trest.utils import is_json_string


class ObjectConverter:
    _log = logging.getLogger(__name__)

    @classmethod
    def to_string(cls, obj: Any, indent: int = None):
        """
        Converts an object to a string representation.
        :param obj: object to convert. Supported types are: dict, dataclass, str, object
        :param indent: indentation level in the string representation for json
        :return:
        """
        cls._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                       f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        if type(obj) == dict:
            string_repr = json.dumps(obj, indent=indent)
        elif is_dataclass(obj):
            string_repr = JTOConverter.to_json(obj)
            string_repr = json.dumps(string_repr, indent=indent)
        elif type(obj) == str:
            if is_json_string(obj):
                string_repr = json.dumps(json.loads(obj), indent=indent)
            else:
                string_repr = obj
        else:
            try:
                string_repr = json.dumps(obj, default=vars, indent=indent)
            except Exception:
                cls._log.error(f'Unexpected body type "{str(type(obj))}" was passed '
                               f'and cannot be converted to string')
                raise ValueError(f'Unexpected body type "{str(type(obj))}" was passed '
                                 f'and cannot be converted to string')
        return string_repr
