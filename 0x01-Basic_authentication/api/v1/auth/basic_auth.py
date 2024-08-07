#!/usr/bin/env python3
"""handle basic auth"""
import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """- defines the attributes and methods for basic
    authorization
    - inherits from Auth
    Args:
        Auth (class): Parent authentication class
    """
