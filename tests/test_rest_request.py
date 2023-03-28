from trest.rest_request import RESTRequest


def test_get_curl_string():
    request = RESTRequest(method='POST', url='https://api.ipify.org',
                          params={'param1': 'one', 'param2': 'two'},
                          headers={'header1': 'one', 'header2': 'four'},
                          body={'body1': 'one', 'body2': 'two'})

    expected = 'curl -X POST -H "header1: one" -H "header2: four" ' \
               '-d \'{"body1": "one", "body2": "two"}\' ' \
               'https://api.ipify.org?param1=one&param2=two'
    assert request.get_curl_string() == expected


# def test_get_curl_string_one_line():
#     request = RESTRequest(method='POST', url='https://api.ipify.org',
#                           params={'param1': 'one', 'param2': 'two'},
#                           headers={'header1': 'one', 'header2': 'four'},
#                           body={'body1': 'one', 'body2': 'two'})
#
#     expected = "curl --location --request POST https://api.ipify.org?param1=one&param2=two " \
#                "--header 'header1: one' --header 'header2: four' " \
#                "--data-raw '{\"body1\": \"one\", \"body2\": \"two\"}'"
#     assert request.get_curl_string(one_line=True) == expected



