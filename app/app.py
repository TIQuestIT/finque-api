import os
from resource.customer import Customer

from flask import Flask
from flask_babel import Babel
from flask_restful import Api

from db import db
from ma import ma


def build_app():
    """Create the flask app and configure ist using classes from 'config.py'."""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config.from_object("config.ConfigSQL")
    app.config.from_object("config.ConfigJWT")
    app.config.from_object("config.ConfigBabel")

    @app.before_first_request
    def create_tables():
        """Create tables before the first request runs, if they do not already exist."""
        print("Creating tables")
        db.create_all()

    return app


def build_babel(app):
    """Initialize Babel."""
    babel = Babel(app)
    return babel


def build_api(app):
    """Initialize flask_restful Api and add resources."""
    api = Api(app)
    api.add_resource(Customer, "/customer/<string:customer_number>")
    return api


def build_app_routes(app):
    """Create routes for non-API pages."""

    @app.route("/")
    def home() -> str:
        return "QuestNet API"


def main() -> None:
    """Initialize the app and all dependencies. Finally run it."""
    app = build_app()
    db.init_app(app)
    ma.init_app(app)
    build_babel(app)
    build_app_routes(app)
    build_api(app)

    app.run(
        debug=os.getenv("DEBUG", default=False),  # type: ignore
        port=os.getenv("PORT", default=5000),  # type: ignore
    )


if __name__ == "__main__":
    main()
