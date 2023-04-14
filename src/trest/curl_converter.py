import inspect
import logging
from typing import Dict, List, Union


class CurlConverter:
    _log = logging.getLogger(__name__)

    @classmethod
    def to_curl(cls, method: str,
                url: str,
                params: Dict[str, Union[str, List[str]]] = None,
                headers: Dict[str, str] = None,
                data: str = None,
                multiline: bool = False) -> str:
        """
        Generates Curl string representation
        :param method: http method
        :param url: url
        :param params: dictionary of url parameters
        :param headers: dict of headers
        :param data: data string
        :return: curl string representation
        """
        cls._log.debug(f'function "{inspect.currentframe().f_code.co_name}" '
                       f'called with args "{inspect.getargvalues(inspect.currentframe()).locals}"')
        if multiline:
            curl_cmd = f'curl -X {method} \\\n'
        else:
            curl_cmd = f'curl -X {method}'

        if headers is not None:
            if multiline:
                headers = ' \\\n'.join(f'-H "{key}: {value}"' for key, value in headers.items())
                curl_cmd += f'{headers} \\\n'
            else:
                headers = ' '.join(f'-H "{key}: {value}"' for key, value in headers.items())
                curl_cmd += f' {headers}'

        if data is not None:
            curl_cmd += f' -d \'{data}\''

        if params is not None:
            params_list = []
            for key, value in params.items():
                if type(value) == list:
                    for item in value:
                        params_list.append(f'{key}={item}')
                else:
                    params_list.append(f'{key}={value}')
            url = f'{url}?'+'&'.join(params_list)
        if multiline:
            curl_cmd += f'{url}'
        else:
            curl_cmd += f' {url}'
        return curl_cmd
