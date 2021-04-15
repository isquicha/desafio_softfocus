from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def init_app(app: Flask):
    """Initiates SQLAlchemy and Migrate on a Flask app


    Parameters
    ----------
    app : Flask
    """
    Migrate(app, db)
    db.init_app(app)
