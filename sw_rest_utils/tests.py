# coding: utf-8
from unittest import mock
import collections
import requests
import random

from . import RestException


class BaseRestMixin:
    rest_class = None
    rest_class_params = None  # dict
    rest_method_request = None  # get, post, put ...

    def get_rest_class_params(self):
        return self.rest_class_params

    def get_json_result(self):
        return {'result': '123'}

    def get_mock_response(self, response_params: dict):
        response = mock.Mock(spec=requests.Response)  # spec_set
        response.configure_mock(**response_params)
        return response

    def get_method(self):
        return self.rest_method_request.lower()

    def test_incorrect_status_code(self):
        with mock.patch('sw_rest_utils.requests.{}'.format(self.get_method())) as request_method_mock:
            incorrect_status_code = 400 + random.randint(1, 199)
            response_params = {'status_code': incorrect_status_code, 'text': 'test_text'}

            request_method_mock.return_value = self.get_mock_response(response_params)

            with self.assertRaises(RestException):
                rest_class_params = self.get_rest_class_params()
                if rest_class_params:
                    instance_rest_class = self.rest_class(**rest_class_params)
                else:
                    instance_rest_class = self.rest_class()
                instance_rest_class.process_request()

            self.assertTrue(request_method_mock.called)

    def test_status_code_200(self):
        with mock.patch('sw_rest_utils.requests.{}'.format(self.get_method())) as request_method_mock:
            response_params = {
                'status_code': 200,
                'text': 'test_text',
                'data': {'test': 'result'},
                'json.return_value': self.get_json_result()  # метод json вызываемый в get_response_result()
            }
            request_method_mock.return_value = self.get_mock_response(response_params)

            rest_class_params = self.get_rest_class_params()
            if rest_class_params:
                instance_rest_class = self.rest_class(**rest_class_params)
            else:
                instance_rest_class = self.rest_class()
            result = instance_rest_class.process_request()

            self.assertEqual(result, response_params['json.return_value'])
            self.assertTrue(request_method_mock.called)

    def test_incorrect_response(self):
        with mock.patch('sw_rest_utils.requests.{}'.format(self.get_method())) as request_method_mock:
            response_params = {
                'status_code': 200,
                'text': 'test_text',
                'data': {'test': 'result'},
            }
            Response = collections.namedtuple('Response', response_params.keys())
            incorrect_response = Response(**response_params)
            request_method_mock.return_value = incorrect_response
            # MOCK add side_effect

            with self.assertRaises(RestException):
                rest_class_params = self.get_rest_class_params()
                if rest_class_params:
                    instance_rest_class = self.rest_class(**rest_class_params)
                else:
                    instance_rest_class = self.rest_class()
                instance_rest_class.process_request()

            self.assertTrue(request_method_mock.called)

