# coding: utf-8
from typing import Dict
from copy import deepcopy
from rest_framework.exceptions import ValidationError


class LoggingMixin:
    log_params = None
    logger = None

    def get_log_params(self, **kwargs) -> Dict:
        params = deepcopy(self.log_params) or {}
        if kwargs:
            params.update(kwargs)
        return params

    def log_error(self, message, **kwargs):
        self.logger.error(message, extra=self.get_log_params(**kwargs))

    def log_warning(self, message, **kwargs):
        self.logger.warning(message, extra=self.get_log_params(**kwargs))

    def log_info(self, message, **kwargs):
        self.logger.info(message, extra=self.get_log_params(**kwargs))

    def log_debug(self, message, **kwargs):
        self.logger.debug(message, extra=self.get_log_params(**kwargs))


class RequestSerializerMixin:
    request_serializer_class = None
    logger = None

    def get_instance(self, request):
        return None

    def get_serializer(self, *args, **kwargs):
        return self.request_serializer_class(*args, **kwargs)

    def validate(self):
        request = self.request
        params = {}
        data = {}
        if hasattr(request, 'data') and request.data:
            data = request.data
        elif hasattr(request, 'query_params') and request.query_params:
            data = request.query_params
        params['data'] = data

        instance = self.get_instance(request)
        if instance is not None:
            params['instance'] = instance

        serializer = self.get_serializer(**params)
        try:
            serializer.is_valid(raise_exception=True)
            return serializer

        except ValidationError as ex:
            log_params = self.get_log_params()
            log_params['serializer_data'] = params['data']

            message = 'Ошибка валидации'
            if log_params.get('message'):
                message += ' (%s)' % log_params.pop('message')

            try:
                validation_details = dict(ex.detail)
                if validation_details.get('non_field_errors'):
                    validation_details['non_field_errors'] = ', '.join(validation_details.pop('non_field_errors'))
                log_params['validation_details'] = validation_details
            except Exception:
                pass

            self.logger.warning(message, extra=log_params, exc_info=True)
            raise

