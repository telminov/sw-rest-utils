# coding: utf-8
from typing import Dict

from rest_framework.exceptions import ValidationError


class LoggingMixin:
    log_params = None
    logger = None

    def get_log_params(self, **kwargs) -> Dict:
        params = self.log_params or {}
        if kwargs:
            params.update(kwargs)
        return params

    def log_warning(self, **kwargs):
        self.logger.warning(self.get_log_params(**kwargs))

    def log_info(self, **kwargs):
        self.logger.info(self.get_log_params(**kwargs))

    def log_debug(self, **kwargs):
        self.logger.debug(self.get_log_params(**kwargs))


class RequestSerializerMixin:
    request_serializer_class = None
    logger = None

    def get_instance(self, request):
        return None

    def get_serializer(self, **params):
        return self.request_serializer_class(**params)

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

        except ValidationError:
            log_params = {'message': 'Ошибка валидации'}
            log_params.update(
                self.get_log_params()
            )

            self.logger.warning(log_params, exc_info=True)
            raise

