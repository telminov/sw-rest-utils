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
    method = 'GET'

    def request(self, url: str, request_kwargs: Dict) -> requests.Response:
        method = self.get_method().lower()
        return getattr(requests, method)(url, **request_kwargs)

    def process_request(self):
        try:
            response = self.request(self.get_url(), self.get_request_kwargs())
            logger.debug({
                'message': self.get_label(),
                'response': {
                    'status_code': response.status_code,
                    'content': response.content,
                }
            })

            if response.status_code < 300:
                return self.get_response_result(response)
            else:
                raise RestException.process_response('Ошибка REST "%s"' % self.get_label(), response)

        except Exception as ex:
            msg = 'Ошибка REST "%s"' % self.get_label()
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

    def get_label(self) -> str:
        if self.label:
            return self.label
        else:
            return str(self.__class__.__name__)

    def get_method(self) -> str:
        return self.method

    def get_request_kwargs(self):
        kwargs = {}

        headers = self.get_headers()
        if headers:
            kwargs['headers'] = headers

        params = self.get_params()
        if params:
            kwargs['params'] = params

        data = self.get_data()
        if data:
            kwargs['data'] = data

        json_data = self.get_json()
        if json_data:
            kwargs['json'] = json_data

        auth_verified_ssl_crt = getattr(settings, 'AUTH_VERIFIED_SSL_CRT_PATH', None)
        kwargs['verify'] = auth_verified_ssl_crt

        return kwargs

    def get_headers(self) -> Dict:
        return None

    def get_params(self) -> Dict:
        return None

    def get_data(self) -> Dict:
        return None

    def get_json(self) -> Dict:
        return None
