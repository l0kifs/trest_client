import json
import logging

from requests import Response

from src.trest.utils import is_json


class RESTResponse(object):
    def __init__(self, response: Response):
        self._log = logging.getLogger(self.__class__.__name__)
        self.url = response.request.url
        self.method = response.request.method
        self.path = response.request.path_url
        self.request_headers = dict(response.request.headers)
        self.request_body = str(response.request.body) if response.request.body else None

        self.status_code = response.status_code
        self.reason = response.reason
        self.response_headers = dict(response.headers)
        self.response_body = str(response.text)
        self.elapsed_time = str(response.elapsed)

    def get_response_body_json(self):
        self._log.info(f'Get response body json')
        if not is_json(self.response_body):
            raise TypeError(f'Response body {self.response_body} is not json')
        return json.loads(self.response_body)

    def get_request_json_repr(self):
        self._log.info(f'Get request json representation')
        json_response = {
            'status_code': self.status_code,
            'reason': self.reason,
            'headers': self.response_headers,
            'elapsed_time': self.elapsed_time,
            'body': self.response_body if not is_json(self.response_body) else json.loads(
                self.response_body)
        }
        json_request = {
            'url': self.url,
            'method': self.method,
            'path': self.path,
            'headers': self.request_headers,
            'body': self.request_body if not is_json(self.request_body) else json.loads(
                self.request_body),
            'response': json_response
        }
        return json_request

    def get_string_repr(self):
        self._log.info(f'Get response string representation')
        result_string = f'{self.status_code} {self.reason} {self.elapsed_time}'

        if self.response_headers:
            result_string = result_string + '\n\nHeaders:\n'
            headers = []
            for key, value in self.response_headers.items():
                headers.append(f"{key}: {value}")
            result_string = result_string + '\n'.join(headers)

        if self.response_body:
            result_string = result_string + '\n\nContent:\n'
            body_string = self.response_body if not is_json(self.response_body) else json.dumps(
                json.loads(self.response_body), indent=4)
            result_string = result_string + body_string

        return result_string
