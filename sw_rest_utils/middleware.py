# coding: utf-8
from djutils.response import JSONResponse
from rest_framework import status
from . import RestException


class RestExceptionMiddleware(object):

    def process_exception(self, request, exception):
        if not isinstance(exception, RestException):
            return None
        return JSONResponse(exception.result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
