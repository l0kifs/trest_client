from trest.curl_converter import CurlConverter


def test_curl_get():
    curl_str = CurlConverter.to_curl('GET', 'https://www.example.com')
    assert curl_str == 'curl -X GET https://www.example.com'


def test_curl_post_json():
    curl_str = CurlConverter.to_curl(method='POST', url='https://www.example.com',
                                     headers={'Content-Type': 'application/json'},
                                     data='{"key1": "value1", "key2": "value2"}')
    assert curl_str == 'curl -X POST -H "Content-Type: application/json" ' \
                       '-d \'{"key1": "value1", "key2": "value2"}\' ' \
                       'https://www.example.com'


def test_simple_params():
    curl_str = CurlConverter.to_curl(method='POST', url='https://www.example.com',
                                     params={'p1': 'v1', 'p2': 'v2'},
                                     headers={'Content-Type': 'application/json'},
                                     data='{"key1": "value1", "key2": "value2"}')
    assert curl_str == 'curl -X POST -H "Content-Type: application/json" ' \
                       '-d \'{"key1": "value1", "key2": "value2"}\' ' \
                       'https://www.example.com?p1=v1&p2=v2'


def test_list_param():
    curl_str = CurlConverter.to_curl(method='POST', url='https://www.example.com',
                                     params={'p1': 'v1', 'p2[]': ['111', '222']},
                                     headers={'Content-Type': 'application/json'},
                                     data='{"key1": "value1", "key2": "value2"}')
    assert curl_str == 'curl -X POST -H "Content-Type: application/json" ' \
                       '-d \'{"key1": "value1", "key2": "value2"}\' ' \
                       'https://www.example.com?p1=v1&p2[]=111&p2[]=222'
