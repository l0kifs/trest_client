from trest.rest_request import RESTRequest


def test_get_curl_string():
    request = RESTRequest(method='POST', url='https://api.ipify.org',
                          params={'param1': 'one', 'param2': 'two'},
                          headers={'header1': 'one', 'header2': 'four'},
                          body={'body1': 'one', 'body2': 'two'})

    expected = "curl --location --request POST https://api.ipify.org?param1=one&param2=two \\\n" \
               "--header 'header1: one' \\\n--header 'header2: four' \\\n" \
               "--data-raw '{\n    \"body1\": \"one\",\n    \"body2\": \"two\"\n}'"
    assert request.get_curl_string() == expected


def test_get_curl_string_one_line():
    request = RESTRequest(method='POST', url='https://api.ipify.org',
                          params={'param1': 'one', 'param2': 'two'},
                          headers={'header1': 'one', 'header2': 'four'},
                          body={'body1': 'one', 'body2': 'two'})

    expected = "curl --location --request POST https://api.ipify.org?param1=one&param2=two " \
               "--header 'header1: one' --header 'header2: four' " \
               "--data-raw '{\"body1\": \"one\", \"body2\": \"two\"}'"
    assert request.get_curl_string(one_line=True) == expected



