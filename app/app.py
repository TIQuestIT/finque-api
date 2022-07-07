from os import getenv

from flask import Flask

from api import api
from api.models.user import user_datastore
from config import config_by_name
from core.babel import babel
from core.bcrypt import flask_bcrypt
from core.db import db
from core.ma import ma
from core.security import security


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    ma.init_app(app)
    flask_bcrypt.init_app(app)
    babel.init_app(app)
    security.init_app(app, user_datastore, register_blueprint=False)
    api.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app(getenv("ENVIRONMENT"))

    @app.before_first_request
    def create_tables():
        print("Creating tables")
        db.create_all()

    app.run(port=getenv("PORT", 5000), debug=getenv("DEBUG", False))  # type: ignore
