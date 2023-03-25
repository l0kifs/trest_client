import inspect
import json
import logging
from typing import Dict

from trest.utils import is_json_string


class RESTResponse(object):
    _log = logging.getLogger(__name__)

    def __init__(self, url: str,
                 method: str,
                 path: str,
                 request_headers: Dict[str, str],
                 request_body: str,
                 status_code: int,
                 reason: str,
                 response_headers: Dict[str, str],
                 response_body: str,
                 elapsed_time: str):
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')

        self.url = url
        self.method = method
        self.path = path
        self.request_headers = request_headers
        self.request_body = request_body

        self.status_code = status_code
        self.reason = reason
        self.response_headers = response_headers
        self.response_body = response_body
        self.elapsed_time = elapsed_time

    def get_response_body_json(self):
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        if not is_json_string(self.response_body):
            raise TypeError(f'Response body {self.response_body} is not json')
        return json.loads(self.response_body)

    def get_request_json_repr(self):
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        json_response = {
            'status_code': self.status_code,
            'reason': self.reason,
            'headers': self.response_headers,
            'elapsed_time': self.elapsed_time,
            'body': self.response_body if not is_json_string(self.response_body) else json.loads(
                self.response_body)
        }
        json_request = {
            'url': self.url,
            'method': self.method,
            'path': self.path,
            'headers': self.request_headers,
            'body': self.request_body if not is_json_string(self.request_body) else json.loads(
                self.request_body),
            'response': json_response
        }
        return json_request

    def get_string_repr(self, one_line: bool = False) -> str:
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        result_string = f'{self.status_code} {self.reason} {self.elapsed_time}'

        if self.response_headers:
            if one_line:
                result_string = result_string + ', Headers: '
                headers = []
                for key, value in self.response_headers.items():
                    headers.append(f"{key}: {value}")
                result_string = result_string + ', '.join(headers)
            else:
                result_string = result_string + '\n\nHeaders:\n'
                headers = []
                for key, value in self.response_headers.items():
                    headers.append(f"{key}: {value}")
                result_string = result_string + '\n'.join(headers)

        if self.response_body:
            if one_line:
                result_string = result_string + ', Content: '
                body_string = self.response_body if not is_json_string(self.response_body) else json.dumps(
                    json.loads(self.response_body))
                result_string = result_string + body_string
            else:
                result_string = result_string + '\n\nContent:\n'
                body_string = self.response_body if not is_json_string(self.response_body) else json.dumps(
                    json.loads(self.response_body), indent=4)
                result_string = result_string + body_string

        return result_string
