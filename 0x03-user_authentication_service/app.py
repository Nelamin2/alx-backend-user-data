#!/usr/bin/env python3
"""Route module for basic flask app API
"""

from db import DB
from flask import Flask, jsonify, request, abort, redirect
from flask.helpers import make_response
from auth import Auth
from user import User

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """GET /
    Returns welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """POST /users, JSON: -email, -password
    Returns end-point to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400

    @app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """POST /sessions, - email, - password
    Returns request with form data with email and password fields
    """
    user_request = request.form
    user_email = user_request.get('email', '')
    user_password = user_request.get('password', '')
    valid_log = AUTH.valid_login(user_email, user_password)
    if not valid_log:
        abort(401)
    response = make_response(jsonify({"email": user_email,
                                      "message": "logged in"}))
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /sessions, - session_id
    Find user with requested session ID, if exists, destroy session
    Redirect user to GET /, if doesnt exists, respond with 403 HTTP
    status
    """
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return 403 if session ID is invalid
    Use session_id to find user
    """
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    return jsonify({"email": user}), 200
