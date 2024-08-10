#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


def get_auth_instance(auth_type):
    """
    Returns an instance of the appropriate authentication class.
    """
    if auth_type == "auth":
        from api.v1.auth.auth import Auth
        return Auth()
    elif auth_type == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        return SessionAuth()
    elif auth_type == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        return BasicAuth()
    return None

auth_type = getenv('AUTH_TYPE')
auth = get_auth_instance(auth_type)


@app.before_request
def before_request():
    """Handler for all requests"""

    if auth is None:
        return

    path = request.path.rstrip('/')
    public_paths = [
        '/api/v1/status',
        '/api/v1/unauthorized',
        '/api/v1/forbidden',
        '/api/v1/auth_session/login'
    ]

    # Check if the path is public
    if path in public_paths:
        return

    # Check authorization header and session cookie
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)  # Unauthorized

    request.current_user = auth.current_user(request)

    # Check current user
    if request.current_user is None:
        abort(403)  # Forbidden


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

