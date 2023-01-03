from trest.rest_request import RESTRequest
from trest.configuration.config import Config


def test_print_one_line_request(capsys):
    Config.one_line_request = True
    Config.print_request_to_std_out = True

    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()

    captured = capsys.readouterr()
    assert len(captured.out) > 2
    assert captured.out.count('\n') == 1


def test_print_one_line_response(capsys):
    Config.one_line_response = True
    Config.print_response_to_std_out = True

    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()

    captured = capsys.readouterr()
    assert len(captured.out) > 2
    assert captured.out.count('\n') == 1
