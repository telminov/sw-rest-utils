# coding: utf-8
from djutils.response import JSONResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from . import RestException


class RestExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        response = None
        if isinstance(exception, RestException):
            if getattr(settings, 'USE_REST_EXCEPTION_VIEW', False):
                next_url = request.META.get('HTTP_REFERER', '')
                refresh_url = request.META.get('PATH_INFO', '')
                params = '?message=%s&next=%s&refresh_url=%s' % (exception, next_url, refresh_url)
                response = redirect(reverse('rest_exception') + params)
                
            else:
                response = JSONResponse(exception.result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response
