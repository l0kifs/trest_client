# TREST client

## Description
Basic REST client with extended logging.

## Features
- Every request provide allure report step with all request and response data.  
Report data organised in a way convenient for testing API and repeating issues in Postman.
- Dataclass objects provided by `jto` library can be used as request body.  
Useful for project organization.
- Client configuration using `Config` module.
  - Print full request and response data to stdout. Useful for fast debugging.
  - Provide oneline representation of request and response. Useful for mor accurate logging.

## Examples

Basic usage:
```python
from trest.rest_request import RESTRequest

request = RESTRequest(method='GET', url='https://api.ipify.org')
response = request.send()
```
Client configuration:
```python
from trest.configuration.config import Config

Config.one_line_response = True
Config.print_response_to_std_out = True
```