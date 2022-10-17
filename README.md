# TREST client

## Description
Basic REST client with extended logging.

## Features
- Every request provide allure report step with all request and response data.  
Report data organised in a way convenient for testing API and repeating issues in Postman.
- Dataclass objects provided by `jto` library can be used as request body.  
Useful for project organization.

## Examples

```python
from trest.rest_request import RESTRequest

request = RESTRequest(method='GET', url='https://api.ipify.org')
response = request.send()
```