from dataclasses import dataclass, field

import allure
from trest.rest_request import RESTRequest


@allure.title("Test get request")
def test_get_request():
    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()


@allure.title("Test post request with dataclass body")
def test_post_request_with_dataclass_body():
    @dataclass
    class Data:
        Id: int = field(default=None, metadata={'name': 'Id', 'required': False})
        Customer: str = field(default=None, metadata={'name': 'Customer', 'required': False})
        Quantity: int = field(default=None, metadata={'name': 'Quantity', 'required': False})
        Price: float = field(default=None, metadata={'name': 'Price', 'required': False})

    headers = {'Content-Type': 'application/json'}
    body = Data(1, 'aaa', 2, 3.33)

    request = RESTRequest(method='POST', url='https://reqbin.com/echo/post/json', headers=headers, body=body)
    response = request.send()
