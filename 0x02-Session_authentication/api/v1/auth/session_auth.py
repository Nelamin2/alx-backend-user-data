#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from uuid import uuid4

from models.user import User
from flask import Blueprint
from .auth import Auth

login = Blueprint('session_auth', __name__, url_prefix='/api/v1/auth_session')


class SessionAuth(Auth):
    """Session authentication class."""

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for the user."""
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None
        # Import Auth here to avoid circular import issue
        from api.v1.auth.auth import Auth
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        print(f"Looking up session ID: {session_id}, found user ID: {user_id}")
        return user_id

    def current_user(self, request=None) -> User:
        """Retrieves the user associated with the request."""
        from api.v1.auth.auth import Auth  # Delay import to avoid circular import
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroys an authenticated session."""
        from api.v1.auth.auth import Auth  # Delay import to avoid circular import
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True