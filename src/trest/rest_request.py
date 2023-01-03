import json
import logging
from dataclasses import is_dataclass
from typing import TypeVar, Generic, Dict

import allure
import requests
from jto import JTOConverter
from requests import Response

from trest.rest_response import RESTResponse
from trest.utils import is_json_string
from trest.configuration.config import Config

T = TypeVar('T')


class RESTRequest(Generic[T]):
    def __init__(self, method: str,
                 url: str,
                 params: Dict[str, str] = None,
                 headers: Dict[str, str] = None,
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
            body_string = json.dumps(body_string, indent=indent)
        elif type(self.body) == str:
            if is_json_string(self.body):
                body_string = json.dumps(json.loads(self.body), indent=indent)
            else:
                body_string = self.body
        else:
            raise ValueError(f'Unexpected body type "{str(type(self.body))}" was passed '
                             f'and cannot be converted to string')
        return body_string

    def get_curl_string(self, one_line: bool = False) -> str:
        self._log.info('Get curl string representation of the request')
        result_string = f'curl --location --request {self.method} {self.url}'

        if self.params:
            result_string = result_string + '?' + '&'.join([f'{key}={val}' for key, val in self.params.items()])

        if self.headers:
            result_string = result_string + ' '
            if not one_line:
                result_string = result_string + '\\\n'
            headers = []
            for key, value in self.headers.items():
                headers.append(f"--header '{key}: {value}'")
            if one_line:
                result_string = result_string + ' '.join(headers)
            else:
                result_string = result_string + ' \\\n'.join(headers)

        if self.body:
            if one_line:
                body_string = self._convert_body_to_string(indent=None)
                result_string = f"{result_string} --data-raw '{body_string}'"
            else:
                body_string = self._convert_body_to_string(indent=4)
                result_string = f"{result_string} \\\n--data-raw '{body_string}'"

        return result_string

    def _create_response(self, response: Response) -> 'RESTResponse':
        self._log.info('Create RESTResponse object')
        return RESTResponse(url=response.request.url,
                            method=response.request.method,
                            path=response.request.path_url,
                            request_headers=dict(response.request.headers),
                            request_body=str(response.request.body) if response.request.body else None,
                            status_code=response.status_code,
                            reason=response.reason,
                            response_headers=dict(response.headers),
                            response_body=str(response.text),
                            elapsed_time=str(response.elapsed))

    def send(self) -> 'RESTResponse':
        self._log.info(f'Send request {self.method} {self.url}')
        with allure.step(f'{self.method} {self.url}'):
            curl_request = self.get_curl_string(one_line=Config.one_line_request)
            try:
                allure.attach(curl_request, 'Request curl', allure.attachment_type.TEXT)
            except Exception as e:
                self._log.warning('Failed to attach request to allure report', stack_info=True)
            self._log.debug(f'Request curl:\n{curl_request}')
            if Config.print_request_to_std_out:
                print(curl_request)
            try:
                response = requests.request(self.method,
                                            self.url,
                                            params=self.params,
                                            headers=self.headers,
                                            data=self._convert_body_to_string() if self.body else None,
                                            hooks=self.hooks,
                                            timeout=self.timeout)

                rest_response = self._create_response(response)
                response_repr = rest_response.get_string_repr(one_line=Config.one_line_response)
                try:
                    allure.attach(response_repr, 'Response', allure.attachment_type.TEXT)
                except Exception as e:
                    self._log.warning('Failed to attach response to allure report', stack_info=True)
                self._log.debug(f'Response string:\n{response_repr}')
                if Config.print_response_to_std_out:
                    print(response_repr)

                return rest_response
            except Exception as e:
                raise e
