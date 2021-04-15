from flask import Flask
from src.extensions.configuration import init_app as configure


def create_app() -> Flask:
    """Creates, configures and returns the `Flask` App

    Returns
    -------
    Flask
        The app
    """
    app = Flask(__name__)
    configure(app=app)

    return app
