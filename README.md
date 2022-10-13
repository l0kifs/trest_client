# TREST client

## Description
Basic REST client with extended logging.

## Examples

```python
from trest.rest_request import RESTRequest

request = RESTRequest(method='GET', url='https://api.ipify.org')
response = request.send()
```