import os
from resource.customer import Customer

from flask import Flask
from flask_babel import Babel
from flask_restful import Api
from omegaconf import DictConfig

from db import db
from ma import ma


def build_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config.from_object("config.ConfigSQL")
    app.config.from_object("config.ConfigJWT")
    app.config.from_object("config.ConfigBabel")

    @app.before_first_request
    def create_tables():
        print("Creating tables")
        db.create_all()

    return app


def build_babel(app):
    babel = Babel(app)
    return babel


def build_api(app):
    api = Api(app)
    api.add_resource(Customer, "/customer/<string:customer_number>")
    return api


def build_app_routes(app):
    @app.route("/")
    def home() -> str:
        return "QuestNet API"


def main() -> None:
    app = build_app()
    db.init_app(app)
    ma.init_app(app)
    build_babel(app)
    build_app_routes(app)
    build_api(app)

    app.run(
        debug=os.getenv("DEBUG", default=False), port=os.getenv("PORT", default=5000)
    )


if __name__ == "__main__":
    main()
