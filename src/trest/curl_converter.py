import inspect
import logging
from typing import Dict


class CurlConverter:
    _log = logging.getLogger(__name__)

    @classmethod
    def to_curl(cls, method: str,
                url: str,
                headers: Dict[str, str] = None,
                data: str = None) -> str:
        """
        Generates Curl string representation
        :param method: http method
        :param url: url
        :param headers: dict of headers
        :param data: data string
        :return: curl string representation
        """
        cls._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                       f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')

        curl_cmd = f'curl -X {method}'
        if headers is not None:
            headers = ' '.join(f'-H "{key}: {value}"' for key, value in headers.items())
            curl_cmd += f' {headers}'
        if data is not None:
            curl_cmd += f' -d \'{data}\''
        curl_cmd += f' {url}'

        return curl_cmd
