#!/usr/bin/env python3
""" Module of authentication
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from typing import List, Type


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """Returns False if the path is in the list of excluded paths,
        otherwise returns True.

        Args:
            path (str): The path to check.
            excluded_paths (list): A list of paths to exclude.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None:
            return True

        for excluded_path in excluded_paths:
            # Handle wildcard at the end of the path
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path or path + '/' == excluded_path:
                return False

        return True

    def current_user(self, request=None) -> Type[User]:
        """ current_user
        """
        if self.authorization_header(request) is None:
            return None
        else:
            User().search({'id': 1})
            return User()

    def authorization_header(
            self,
            request=None
            ) -> str:
        '''Auth header
        '''
        if request is None:
            return None

        return request.headers.get('Authorization')
