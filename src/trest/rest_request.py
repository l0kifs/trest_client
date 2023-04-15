import inspect
import json
import logging
from dataclasses import is_dataclass
from typing import TypeVar, Generic, Dict, Union, List

import allure
import requests
from jto import JTOConverter
from requests import Response
from trest.curl_converter import CurlConverter
from trest.object_converter import ObjectConverter

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

        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.body: T = body
        self.hooks = hooks
        self.timeout = timeout

        self.response: Union[RESTResponse, None] = None

    def get_json(self, indent: int = None) -> str:
        """
        Get json representation of the request.
        :param indent: integer of indentation
        :return:
        """
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        return json.dumps(self, default=vars, indent=indent)

    def _convert_body_to_string(self, indent: int = None) -> str:
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        body_string = ObjectConverter.to_string(self.body, indent=indent)
        return body_string

    def get_curl_string(self) -> str:
        """
        Get curl string representation of the request.
        :return:
        """
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        result_string = CurlConverter.to_curl(method=self.method,
                                              url=self.url,
                                              params=self.params,
                                              headers=self.headers,
                                              data=self._convert_body_to_string(indent=None)
                                              if self.body is not None else None,
                                              multiline=False if Config.one_line_request else True)
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
        response_repr = self.response.get_string_repr(one_line=Config.one_line_response) if self.response is not None \
            else 'Response not available'

        self._log.debug(f'Request curl:\n{curl_request}')
        self._log.debug(f'Response string:\n{response_repr}')

        if Config.print_request_to_std_out:
            print(curl_request)
        if Config.print_response_to_std_out:
            print(response_repr)

        if to_allure:
            with allure.step(f'{self.method} {self.url}'):
                try:
                    allure.attach(curl_request, f'Request curl', allure.attachment_type.TEXT)
                    allure.attach(response_repr, f'Response', allure.attachment_type.TEXT)
                except Exception:
                    self._log.warning('Failed to attach data to allure report', stack_info=True)

    def send(self, to_allure: bool = True) -> 'RESTResponse':
        """
        Sends the request and returns the response.
        :param to_allure: flag to enable/disable allure reporting for this request
        :return: response object
        """
        self._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                        f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        try:
            response = requests.request(self.method,
                                        self.url,
                                        params=self.params,
                                        headers=self.headers,
                                        data=self._convert_body_to_string() if self.body else None,
                                        hooks=self.hooks,
                                        timeout=self.timeout)
            rest_response = self._create_response(response)
            self.response = rest_response
            return rest_response
        except Exception:
            self._log.error(f'Failed to send request "{self.method} {self.url}"', exc_info=True)
            raise Exception(f'Failed to send request "{self.method} {self.url}"')
        finally:
            self._log_request(to_allure=to_allure)
