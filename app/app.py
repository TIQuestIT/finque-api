import os
from resource.customer import Customer

import hydra
from flask import Flask
from flask_restful import Api
from omegaconf import DictConfig

from db import db
from ma import ma


def build_app(cfg):
    app = Flask(__name__)
    app.secret_key = cfg.app.secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.db.database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_SECRET_KEY"] = cfg.jwt.secret_key
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_ACCESS"] = ["access", "refresh"]

    @app.before_first_request
    def create_tables():
        print("Creating tables")
        db.create_all()

    return app


def build_api(app):
    api = Api(app)
    api.add_resource(Customer, "/customer/<string:name>")
    return api


def build_app_routes(app):
    @app.route("/")
    def home() -> str:
        return "QuestNet API"


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    app = build_app(cfg)
    db.init_app(app)
    ma.init_app(app)
    build_app_routes(app)
    build_api(app)

    app.run(debug=cfg.app.debug, port=cfg.app.port)


if __name__ == "__main__":
    main()
