#!/ usr/ bin / env python3
"""  session_auth module    """
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar
from flask import request
from os import getenv

class SessionAuth(Auth):
    """ SessionAuth class
    """
    pass
