# coding: utf-8
from typing import Dict
import logging
from django.conf import settings
import requests

logger = logging.getLogger('sw.rest')


class RestException(Exception):
    def __init__(self, msg: str, result: Dict = None):
        super().__init__(msg)
        self.result = result or {'error': msg}

    @classmethod
    def process_response(cls, msg: str, response: requests.Response) -> 'RestException':
        result = {
            'error': msg,
            'status_code': response.status_code,
        }

        try:
            result['detail'] = response.json()
        except Exception:
            pass

        ex = cls(msg, result)
        return ex


class BaseRest:
    url = None
    label = None

    def request(self, url: str, request_kwargs: Dict) -> requests.Response:
        return requests.get(url, **request_kwargs)

    def process_request(self):
        try:
            response = self.request(self.get_url(), self.get_request_kwargs())
            logger.debug({
                'message': self.label,
                'response': {
                    'status_code': response.status_code,
                    'text': response.text,
                }
            })

            if response.status_code == 200:
                return self.get_response_result(response)
            else:
                raise RestException.process_response('Ошибка REST "%s"' % self.label, response)

        except Exception as ex:
            msg = 'Ошибка REST "%s"' % self.label
            logger.exception({'message': msg}, exc_info=True)

            if isinstance(ex, RestException):
                raise ex
            else:
                raise RestException(msg) from ex

    @staticmethod
    def get_response_result(response: requests.Response):
        return response.json()

    def get_url(self) -> str:
        return self.url

    def get_request_kwargs(self):
        kwargs = {
            'headers': {'Authorization': 'TokenService {0}'.format(settings.AUTH_TOKEN)}
        }
        auth_verified_ssl_crt = getattr(settings, 'AUTH_VERIFIED_SSL_CRT_PATH', None)
        if auth_verified_ssl_crt:
            kwargs['verify'] = auth_verified_ssl_crt

        params = self.get_params()
        if params:
            kwargs['params'] = params

        data = self.get_data()
        if data:
            kwargs['data'] = data

        return kwargs

    def get_params(self) -> Dict:
        return None

    def get_data(self) -> Dict:
        return None
