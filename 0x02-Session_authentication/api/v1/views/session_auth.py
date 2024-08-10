#!/usr/bin/env python3
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """Handle the session authentication login."""

    # Retrieve email and password from the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    user_list = User.search({'email': email})

    # If no user is found for this email
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    user = user_list[0]

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID for the User ID
    session_id = auth.create_session(user.id)

    # Return the User's JSON representation
    response = jsonify(user.to_json())

    # Set the session ID in the cookie
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
