from functools import wraps
from os import getenv
from time import time

import jwt
from flask import request
from flask_simplelogin import SimpleLogin
from werkzeug.security import check_password_hash, generate_password_hash

from src.utils import json_response
from src.extensions.database import db
from src.models import User


class InvalidUserError(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass


class AlreadyRegisteredError(Exception):
    pass


def token_required(func: callable) -> callable:
    """Protect a view requiring an access token

    `ATTENTION`: The view must receive **kwargs

    Parameters
    ----------
    func : callable
        The function to be protected

    Returns
    -------
    callable
        The protected function
    """

    @wraps(func)
    def inner(*args, **kwargs):
        token = request.args.get("access_token", None)
        if not token:
            body = request.get_json()
            if body is not None:
                token = body.get("access_token", None)
        if not token:
            return json_response(
                status_code=401,
                message="An access_token parameter must be provided",
            )

        try:
            token_information = jwt.decode(
                token, getenv("SECRET_KEY"), algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return json_response(
                status_code=401, message="Expired access_token"
            )
        except jwt.InvalidTokenError:
            return json_response(
                status_code=403, message="Invalid access_token"
            )
        except Exception:
            return json_response(
                status_code=500, message="Error processing access_token"
            )

        return func(*args, **kwargs, token_information=token_information)

    return inner


def verify_login(user: dict) -> bool:
    """Validate username and password to verify user login


    Parameters
    ----------
    user : dict
        Must have `username` and `password` keys

    Returns
    -------
    bool
        True if username and password exists and are correct, False otherwise
    """
    username = user.get("username")
    password = user.get("password")
    if not username or not password:
        return False
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return False
    if check_password_hash(existing_user.password, password):
        return True
    return False


def create_user(username: str, password: str, name: str = "") -> User:
    """Creates a new user


    Parameters
    ----------
    username : str
        The name that will be used to log in
    password : str
        The password that will be used to log in
    name : str, optional
        The name that will be displayed in panel, by default ''

    Returns
    -------
    User
        The new created user object

    Raises
    ------
    AlreadyRegisteredError
        If the username is already registered
    """
    if User.query.filter_by(username=username).first():
        raise AlreadyRegisteredError(f"{username} already exists!")
    user = User(
        username=username, password=generate_password_hash(password), name=name
    )
    db.session.add(user)
    db.session.commit()
    return user


def generate_token(username: str = "", password: str = "") -> bytes:
    """Generates a token for a given user

    Checks the username and password in database
    If they are ok, creates and returns a web token valid for 3 hours
    The SECRET_KEY env var is used as the jwt encoding key

    Parameters
    ----------
    username : str
        The username to generate a token from
    password : str
        The user's password

    Returns
    -------
    bytes
        Token: `jwt.encode()` response

    Raises
    ------
    InvalidUserError
        If the user doesn't exists
    IncorrectPasswordError
        If the password is incorrect
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUserError()
    if not check_password_hash(user.password, password):
        raise IncorrectPasswordError()

    token = jwt.encode(
        {
            "username": username,
            "exp": time() + (3 * 60 * 60),
        },
        key=getenv("SECRET_KEY"),
    )

    return token


def init_app(app):
    SimpleLogin(app, login_checker=verify_login)
