from mock_api_server import MockApiServer
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
               '-d \'{\n    "key1": "value1",\n    "key2": "value2"\n}\' \\\n' \
               'https://www.example.com?key1=value1&key2=value2\n'
    actual = capsys.readouterr().out
    assert actual == expected


def test_print_oneline_request(capsys):
    Config.one_line_request = True
    Config.print_request_to_std_out = True

    request = RESTRequest(method='POST', url='https://www.example.com',
                          params={'key1': 'value1', 'key2': 'value2'},
                          headers={'Content-Type': 'application/json'},
                          body='{"key1": "value1", "key2": "value2"}')
    response = request.send()

    expected = 'curl -X POST -H "Content-Type: application/json" ' \
               '-d \'{"key1": "value1", "key2": "value2"}\' ' \
               'https://www.example.com?key1=value1&key2=value2\n'
    actual = capsys.readouterr().out
    assert actual == expected


def test_print_multiline_response(capsys):
    Config.one_line_response = False
    Config.print_response_to_std_out = True

    request = RESTRequest(method='POST', url='http://localhost:5000/api/return_request',
                          params={'key1': 'value1', 'key2': 'value2'},
                          headers={'Content-Type': 'application/json'},
                          body='{"key1": "value1", "key2": "value2"}')
    with MockApiServer():
        request.send()

    actual = capsys.readouterr().out
    assert len(actual) > 2
    assert actual.strip().count('\n') > 1


def test_print_oneline_response(capsys):
    Config.one_line_response = True
    Config.print_response_to_std_out = True

    request = RESTRequest(method='POST', url='http://localhost:5000/api/return_request',
                          params={'key1': 'value1', 'key2': 'value2'},
                          headers={'Content-Type': 'application/json'},
                          body='{"key1": "value1", "key2": "value2"}')
    with MockApiServer():
        request.send()

    actual = capsys.readouterr().out
    assert len(actual) > 2
    assert actual.strip().count('\n') <= 1
