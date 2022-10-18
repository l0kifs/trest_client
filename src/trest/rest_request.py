import json
import logging
from dataclasses import is_dataclass
from typing import TypeVar, Generic

import allure
import requests
from jto import JTOConverter
from trest.rest_response import RESTResponse

from trest.utils import is_json_string

T = TypeVar('T')


class RESTRequest(Generic[T]):
    def __init__(self, method: str,
                 url: str,
                 params: dict = None,
                 headers: dict = None,
                 body: T = None,
                 hooks: dict = None,
                 timeout: float = None):
        self._log = logging.getLogger(self.__class__.__name__)
        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.body: T = body
        self.hooks = hooks
        self.timeout = timeout

    def get_json(self, indent: int = None) -> str:
        self._log.info('Get json representation of the request')
        return json.dumps(self, default=vars, indent=indent)

    def _convert_body_to_string(self, indent: int = None) -> str:
        self._log.info('Convert request body to string')
        if type(self.body) == dict:
            body_string = json.dumps(self.body, indent=indent)
        elif is_dataclass(self.body):
            body_string = JTOConverter.to_json(self.body)
            print(body_string, '- test')
            body_string = json.dumps(body_string, indent=indent)
            print(body_string, '- test2')
        elif type(self.body) == str:
            if is_json_string(self.body):
                body_string = json.dumps(json.loads(self.body), indent=indent)
            else:
                body_string = self.body
        else:
            raise ValueError(f'Unexpected body type "{str(type(self.body))}" was passed '
                             f'and cannot be converted to string')
        return body_string

    def get_curl_string(self):
        self._log.info('Get curl string representation of the request')
        result_string = f'curl --location --request {self.method} {self.url}'

        if self.params:
            result_string = result_string + '?' + '&'.join([f'{key}={val}' for key, val in self.params.items()])

        if self.headers:
            result_string = result_string + ' \\\n'
            headers = []
            for key, value in self.headers.items():
                headers.append(f"--header '{key}: {value}'")
            result_string = result_string + ' \\\n'.join(headers)

        if self.body:
            body_string = self._convert_body_to_string(indent=4)
            result_string = f"{result_string} \\\n--data-raw '{body_string}'"

        return result_string

    def send(self) -> 'RESTResponse':
        self._log.info(f'Send request {self.method} {self.url}')
        with allure.step(f'{self.method} {self.url}'):
            allure.attach(self.get_curl_string(), 'Request curl', allure.attachment_type.TEXT)
            self._log.debug(f'Request curl:\n{self.get_curl_string()}')
            try:
                response = requests.request(self.method,
                                            self.url,
                                            params=self.params,
                                            headers=self.headers,
                                            data=self._convert_body_to_string() if self.body else None,
                                            hooks=self.hooks,
                                            timeout=self.timeout)

                rest_response = RESTResponse(response)

                allure.attach(rest_response.get_string_repr(), 'Response', allure.attachment_type.TEXT)
                self._log.debug(f'Response string:\n{rest_response.get_string_repr()}')

                return rest_response
            except Exception as e:
                raise e
