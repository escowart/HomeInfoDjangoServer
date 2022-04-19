"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from typing import Literal

HTTPMethod = Literal["get", "options", "head", "post", "put", "patch", "delete"]


class NonDBModel(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
