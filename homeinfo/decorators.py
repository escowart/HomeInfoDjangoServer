"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from functools import wraps

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from homeinfo.services.logging import log_exception


def api_view_except_all():
    def decorator(func):
        @wraps(func)
        def func_wrapper(self, request: Request, *args, **kwargs) -> Response:
            try:
                return func(self, request, *args, **kwargs)
            except Exception as e:
                log_exception(e)
                return Response(
                    f"Oops! something went wrong. Please contact us for assistance at ${settings.SUPPORT_PHONE_NUMBER}!",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return func_wrapper

    return decorator


def api_view_requires_query_param(*required_query_keys: str):
    def decorator(func):
        @wraps(func)
        def func_wrapper(self, request: Request, *args, **kwargs) -> Response:
            missing_keys = [
                key for key in required_query_keys if key not in request.query_params
            ]
            if len(missing_keys) > 0:
                return Response(
                    f"Missing require query param(s): {missing_keys}",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return func(self, request, *args, **kwargs)

        return func_wrapper

    return decorator
