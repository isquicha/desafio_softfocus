from flask import request
from flask.views import MethodView

from src.utils import json_response
from src.extensions.authentication import (
    create_user,
    generate_token,
    token_required,
    AlreadyRegisteredError,
    InvalidUserError,
    IncorrectPasswordError,
)


class UserAPI(MethodView):
    @token_required
    def post(self, **kwargs):
        body = request.get_json()
        if body is None:
            return json_response(
                status_code=400, message="You must provide a json body"
            )

        username = body.get("username", None)
        password = body.get("password", None)
        name = body.get("name", None)

        if username is None:
            return json_response(
                status_code=400, message="Field 'username' must not be empty"
            )
        if password is None:
            return json_response(
                status_code=400, message="Field 'password' must not be empty"
            )

        try:
            user = create_user(username=username, password=password, name=name)
            payload = {
                "id": user.id,
                "username": user.username,
                "name": user.name,
            }
            return json_response(status_code=201, payload=payload)
        except AlreadyRegisteredError:
            return json_response(
                status_code=400,
                message=f"Username {username} is already registered",
            )
        except Exception:
            return json_response(
                status_code=500, message="Could not create user"
            )


class UserTokenAPI(MethodView):
    def post(self):
        """Tries to get user's access token"""
        body = request.get_json()
        if body is None:
            return json_response(
                status_code=400, message="A JSON body must be provided"
            )

        username = body.get("username", None)
        password = body.get("password", None)

        if username is None:
            return json_response(
                status_code=400, message="Field 'username' must not be empty"
            )
        if password is None:
            return json_response(
                status_code=400, message="Field 'password' must not be empty"
            )

        try:
            token = generate_token(username=username, password=password)
        except (InvalidUserError, IncorrectPasswordError):
            return json_response(
                # ! Don't say to hackers if it is the username that doesn't
                # ! exists or if the password is incorrect.
                status_code=400,
                message="Invalid username or password",
            )
        else:
            return json_response(
                message="Token successful generated",
                payload={"access_token": token},
            )
