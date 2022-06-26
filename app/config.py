"""Flask config."""
from os import getenv, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    DEBUG = getenv("DEBUG")
    PORT = getenv("PORT")
    SECRET_KEY = getenv("SECRET_KEY")


class ConfigSQL:
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True


class ConfigJWT:
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_ACCESS = ["access", "refresh"]


class ConfigBabel:
    BABEL_DEFUALT_LOCALE = getenv("BABEL_DEFUALT_LOCALE")
    BABEL_DEFAULT_TIMEZONE = getenv("BABEL_DEFAULT_TIMEZONE")
