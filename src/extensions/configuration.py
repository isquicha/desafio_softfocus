import os
from dotenv import load_dotenv
from importlib import import_module

from flask import Flask

config = {
    "DEFAULT": {
        "TITLE": "from .env",
        "DEBUG": False,
        "SECRET_KEY": "from .env",
        "PASSWORD_SCHEMES": ["pbkdf2_sha512", "md5_crypt"],
        "SQLALCHEMY_DATABASE_URI": "from .env",
    },
    "DEVELOPMENT": {
        "DEBUG": True,
    },
    "TESTING": {
        "TESTING": True,
    },
    "PRODUCTION": {
        "DEBUG": False,
        "TESTING": False,
    },
}

extensions = {
    "DEFAULT": ["database", "authentication"],
    "DEVELOPMENT": [],
    "TESTING": [],
    "PRODUCTION": [],
}

blueprints = {
    "DEFAULT": [],
    "DEVELOPMENT": [],
    "TESTING": [],
    "PRODUCTION": [],
}


load_dotenv()
env = os.environ.get("FLASK_ENV")
if env is not None:
    env = env.upper()


def init_app(app: Flask) -> bool:
    """Configure flask app

    Loads app configurations, extensions and blueprints, based on settings.py

    Parameters
    ----------
    app : Flask

    Returns
    -------
    bool
        Error flag. True if there is any error occurs
    """
    error = False

    if not load_configuration(app):
        error = True
    if not load_extensions(app):
        error = True
    if not load_blueprints(app):
        error = True

    return error


def load_configuration(app: Flask) -> bool:
    """Loads app configurations


    Parameters
    ----------
    app : Flask

    Returns
    -------
    bool
        Error flag. True if there is any error occurs
    """
    error = False

    def _load_configuration(env):
        for key, value in config[env].items():
            env_value = os.environ.get(key)
            if env_value:
                app.config[key] = env_value
            else:
                app.config[key] = value

    _load_configuration("DEFAULT")
    if env:
        try:
            _load_configuration(env)
        except Exception as e:
            print(f"ERROR\n{e}")
            error = True

    return error


def load_extensions(app: Flask) -> bool:
    """Loads app extensions


    Parameters
    ----------
    app : Flask

    Returns
    -------
    bool
        Error flag. True if there is any error occurs
    """
    error = False

    extensions_path = app.config.get("EXTENSIONS_PATH")
    if extensions_path is None:
        extensions_path = "src.extensions"

    def _load_extensions(env):
        for extension in extensions[env]:
            if extension.find(":") != -1:
                module_name, factory = extension.split(":")
            else:
                module_name = extension
                factory = "init_app"

            try:
                module = import_module(extensions_path + "." + module_name)
            except ImportError:
                module = import_module(module_name)

            module_create = getattr(module, factory)
            module_create(app)

    _load_extensions("DEFAULT")
    if env:
        try:
            _load_extensions(env)
        except Exception as e:
            print(f"ERROR\n{e}")
            error = True

    return error


def load_blueprints(app: Flask) -> bool:
    """Loads app blueprints


    Parameters
    ----------
    app : Flask

    Returns
    -------
    bool
        Error flag. True if there is any error occurs
    """
    error = False

    blueprints_path = app.config.get("BLUEPRINTS_PATH")
    if blueprints_path is None:
        blueprints_path = "src.blueprints"

    def _load_blueprints(env):
        for blueprint in blueprints[env]:
            if blueprint.find(":") != -1:
                module_name, factory = blueprint.split(":")
            else:
                module_name = blueprint
                factory = "init_app"

            module = import_module(blueprints_path + "." + module_name)
            module_create = getattr(module, factory)
            module_create(app)

    _load_blueprints("DEFAULT")
    if env:
        try:
            _load_blueprints(env)
        except Exception as e:
            print(f"ERROR\n{e}")
            error = True

    return error
