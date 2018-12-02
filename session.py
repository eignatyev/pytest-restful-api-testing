import json
from requests import RequestException, Session

from logger import Logger
from singleton import Singleton


class HTTPSession(Session):

    URL = 'https://jsonplaceholder.typicode.com/'

    @staticmethod
    def send_request(request_type, endpoint, **params):
        do_logging = params.pop('do_logging', True)
        try:
            response = request_type(endpoint, **params)
            if do_logging:
                Logger.log_request(request_type, endpoint, params, response.status_code)
            return response.status_code, json.loads(response.text)
        except RequestException as e:
            Logger.log_exception('Could not send {} request due to exception: {}'.format(request_type, e))

class RequestTypes:
    GET = HTTPSession().get
    POST = HTTPSession().post

class Endpoints:
    ALBUMS = HTTPSession.URL + 'albums'
    USERS = HTTPSession.URL + 'users'

class StatusCodes:
    STATUS_200 = '200'
