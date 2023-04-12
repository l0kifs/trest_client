import inspect
import json
import logging
from dataclasses import is_dataclass
from typing import TypeVar, Generic, Dict, Union, List

import allure
import requests
from allure_commons._allure import StepContext
from jto import JTOConverter
from requests import Response
from trest.curl_converter import CurlConverter

from trest.rest_response import RESTResponse
from trest.configuration.config import Config
from trest.utils import is_json_string

T = TypeVar('T')


class RESTRequest(Generic[T]):
    _log = logging.getLogger(__name__)

    def __init__(self, method: str,
                 url: str,
                 params: Dict[str, Union[str, List[str]]] = None,
                 headers: Dict[str, str] = None,
                 body: T = None,
                 hooks: dict = None,
                 timeout: float = None):
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        self._allure_step = None

        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.body: T = body
        self.hooks = hooks
        self.timeout = timeout

    def get_json(self, indent: int = None) -> str:
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        return json.dumps(self, default=vars, indent=indent)

    def _convert_body_to_string(self, indent: int = None) -> str:
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
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

    def get_curl_string(self) -> str:
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        result_string = CurlConverter.to_curl(method=self.method,
                                              url=self.url,
                                              params=self.params,
                                              headers=self.headers,
                                              data=self._convert_body_to_string(indent=None)
                                              if self.body is not None else None)
        return result_string

    def _create_response(self, response: Response) -> 'RESTResponse':
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
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

    def _log_request(self, to_allure: bool = True) -> None:
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        curl_request = self.get_curl_string()

        self._log.debug(f'Request curl:\n{curl_request}')

        if Config.print_request_to_std_out:
            print(curl_request)

        if to_allure:
            self._allure_step = allure.step(f'{self.method} {self.url}')
            with self._allure_step:
                try:
                    allure.attach(curl_request, 'Request curl', allure.attachment_type.TEXT)
                except Exception as e:
                    self._log.warning('Failed to attach request to allure report', stack_info=True)

    def _log_response(self, rest_response, to_allure: bool = True) -> None:
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        response_repr = rest_response.get_string_repr(one_line=Config.one_line_response)

        self._log.debug(f'Response string:\n{response_repr}')

        if Config.print_response_to_std_out:
            print(response_repr)

        if to_allure:
            with self._allure_step:
                try:
                    allure.attach(response_repr, 'Response', allure.attachment_type.TEXT)
                except Exception as e:
                    self._log.warning('Failed to attach response to allure report', stack_info=True)

    def send(self, to_allure: bool = True) -> 'RESTResponse':
        """
        Sends the request and returns the response.
        :param to_allure: flag to enable/disable allure reporting for this request
        :return: response object
        """
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        self._log_request(to_allure=to_allure)
        try:
            response = requests.request(self.method,
                                        self.url,
                                        params=self.params,
                                        headers=self.headers,
                                        data=self._convert_body_to_string() if self.body else None,
                                        hooks=self.hooks,
                                        timeout=self.timeout)
            rest_response = self._create_response(response)
            self._log_response(rest_response, to_allure=to_allure)
            return rest_response
        except Exception as e:
            raise e
