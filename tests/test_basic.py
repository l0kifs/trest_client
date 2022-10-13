import allure
from trest.rest_request import RESTRequest


@allure.title("Test get request")
def test_get_request():
    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()
