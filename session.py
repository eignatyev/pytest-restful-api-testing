from requests import RequestException, Session

from logger import Logger
from singleton import Singleton


class HTTPSession(Singleton, Session):

    URL = 'https://jsonplaceholder.typicode.com/'

    @staticmethod
    def send_request(request_type, endpoint, **params):
        try:
            response = request_type(endpoint, **params)
            Logger.log_request(request_type, endpoint, params, response.status_code)
            return response
        except RequestException as e:
            Logger.log_exception('Could not send {} request due to exception: {}'.format(request_type, e.message))

request_types = type('RequestTypes', (object,), dict())
request_types.GET = HTTPSession().get
request_types.POST = HTTPSession().post

endpoints = type('Endpoints', (object,), dict())
endpoints.ALBUMS = HTTPSession.URL + 'albums'
endpoints.USERS = HTTPSession.URL + 'users'

print(HTTPSession.send_request(request_type=request_types.GET, endpoint=endpoints.ALBUMS).text)
