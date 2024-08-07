#!/usr/bin/env python3
""" Module of authentication
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def current_user(self, request=None) -> Type[User]:
        """ current_user
        """
        if self.authorization_header(request) is None:
            return None
        else:
            User().search({'id': 1})
