from trest.curl_converter import CurlConverter


def test_curl_get():
    curl_str = CurlConverter.to_curl('GET', 'https://www.example.com')
    assert curl_str == 'curl -X GET https://www.example.com'


def test_curl_post_json():
    curl_str = CurlConverter.to_curl('POST', 'https://www.example.com',
                                     {'Content-Type': 'application/json'},
                                     '{"key1": "value1", "key2": "value2"}')
    assert curl_str == 'curl -X POST -H "Content-Type: application/json" ' \
                       '-d \'{"key1": "value1", "key2": "value2"}\' https://www.example.com'
