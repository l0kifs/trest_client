from trest.rest_request import RESTRequest
from trest.configuration.config import Config


def test_print_multiline_request(capsys):
    Config.one_line_request = False
    Config.print_request_to_std_out = True

    request = RESTRequest(method='POST', url='https://www.example.com',
                          params={'key1': 'value1', 'key2': 'value2'},
                          headers={'Content-Type': 'application/json'},
                          body='{"key1": "value1", "key2": "value2"}')
    response = request.send()

    expected = 'curl -X POST \\\n' \
               '-H "Content-Type: application/json" \\\n' \
               '-d \'{    \n"key1": "value1",    \n"key2": "value2"\n}\' \\\n' \
               'https://www.example.com?key1=value1&key2=value2'

    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == expected
    # assert len(captured.out) > 2
    # assert captured.out.count('\n') == 1


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
    assert captured.out.strip().count('\n') > 1


def test_print_oneline_response(capsys):
    Config.one_line_response = True
    Config.print_response_to_std_out = True

    request = RESTRequest(method='GET', url='https://api.ipify.org')
    response = request.send()

    captured = capsys.readouterr()
    assert len(captured.out) > 2
    assert captured.out.strip().count('\n') == 1
