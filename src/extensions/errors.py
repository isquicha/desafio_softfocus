from flask import Flask
from src.utils import json_response


def init_app(app: Flask):
    @app.errorhandler(405)
    def method_not_allowed(e):
        return json_response(405)

    @app.errorhandler(400)
    def bad_request(e):
        return json_response(400)
