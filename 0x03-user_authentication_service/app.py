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
