#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

# Check environment variable to configure auth
AUTH_TYPE = os.getenv('AUTH_TYPE')

if AUTH_TYPE:
    # Dynamically import Auth class based on AUTH_TYPE
    from api.v1.auth.auth import Auth
    auth = Auth()

if getenv('AUTH_TYPE') == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

elif getenv('AUTH_TYPE') == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    if auth is None:
        return

    # Define public paths
    public_paths = ['/api/v1/status',
                    '/api/v1/unauthorized', '/api/v1/forbidden']

    if request.path in public_paths:
        return

    # Check authorization header
    if auth.authorization_header(request) is None:
        abort(401)  # Unauthorized

    # Check current user
    if auth.current_user(request) is None:
        abort(403)  # Forbidden


@app.errorhandler(401)  # Unauthorized
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)  # Forbidden
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
