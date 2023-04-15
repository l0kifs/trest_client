from multiprocessing import Process
from typing import Union

from flask import jsonify, Flask, request, make_response

app = Flask(__name__)


@app.route('/api/return_request', methods=['GET', 'POST'])
def return_request():
    headers = request.environ
    data = request.data

    response = make_response(data)
    response.headers = headers
    return response


class MockApiServer:
    def __init__(self, port: int = 5000):
        self._server: Union[Process, None] = None
        self._port: int = port

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def _start_app(self):
        app.run(port=self._port)

    def start(self):
        self._server = Process(target=self._start_app)
        self._server.start()
        return self

    def stop(self):
        self._server.terminate()
        self._server.join()
