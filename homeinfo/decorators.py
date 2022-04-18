"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from functools import wraps

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


def api_view_requires_query_param(*required_query_keys: str):
    def decorator(func):
        @wraps(func)
        def func_wrapper(self, request: Request, *args, **kwargs) -> Response:
            for key in required_query_keys:
                return Response(
                    f"Missing require query param: ${key}",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return func(self, request, *args, **kwargs)

        return func_wrapper

    return decorator
