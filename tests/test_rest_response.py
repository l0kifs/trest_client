from trest.rest_response import RESTResponse


def test_get_string_repr():
    response = RESTResponse(url='https://api.ipify.org', method='GET', path='/foo',
                            request_headers={'header1': 'value1', 'header2': 'value2'},
                            request_body='{"body1":"value1"}', status_code=200,
                            reason='ok', response_headers={'header1': 'value1', 'header2': 'value2'},
                            response_body='{"body1":"value1"}', elapsed_time='0.123')

    expected = '200 ok 0.123\n\nHeaders:\nheader1: value1\nheader2: value2\n\n' \
               'Content:\n{\n    "body1": "value1"\n}'
    assert response.get_string_repr() == expected


def test_get_string_repr_one_line():
    response = RESTResponse(url='https://api.ipify.org', method='GET', path='/foo',
                            request_headers={'header1': 'value1', 'header2': 'value2'},
                            request_body='{"body1":"value1"}', status_code=200,
                            reason='ok', response_headers={'header1': 'value1', 'header2': 'value2'},
                            response_body='{"body1":"value1"}', elapsed_time='0.123')

    expected = '200 ok 0.123, Headers: header1: value1, header2: value2, ' \
               'Content: {"body1": "value1"}'
    assert response.get_string_repr(one_line=True) == expected
