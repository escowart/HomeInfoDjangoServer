"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from typing import Literal

import requests
import requests.exceptions
import rest_framework.response

HTTPMethod = Literal["get", "options", "head", "post", "put", "patch", "delete"]


def to_rest_framework_response(
    response: requests.Response,
) -> rest_framework.response.Response:
    try:
        content = response.json()
    except requests.exceptions.JSONDecodeError:
        content = response.content

    return rest_framework.response.Response(
        content,
        status=response.status_code,
        content_type=response.headers.get("content_type"),
    )


class NonDBModel(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
