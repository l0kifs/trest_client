from trest.rest_request import RESTRequest
from trest.configuration.config import Config


def test_print_multiline_request(capsys):
    Config.print_request_to_std_out = True

    request = RESTRequest(method='GET', url='https://api.ipify.org', headers={'accept': 'text/html'})
    response = request.send()

    captured = capsys.readouterr()
    assert len(captured.out) > 2
    assert captured.out.count('\n') > 1


def test_print_oneline_request(capsys):
    Config.one_line_request = True
    Config.print_request_to_std_out = True

    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()

    captured = capsys.readouterr()
    assert len(captured.out) > 2
    assert captured.out.count('\n') == 1


def test_print_multiline_response(capsys):
    Config.print_response_to_std_out = True

    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()

    captured = capsys.readouterr()
    assert len(captured.out) > 2
    assert captured.out.count('\n') > 1


def test_print_oneline_response(capsys):
    Config.one_line_response = True
    Config.print_response_to_std_out = True

    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()

    captured = capsys.readouterr()
    assert len(captured.out) > 2
    assert captured.out.count('\n') == 1
