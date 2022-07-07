"""Flask config."""
from os import getenv, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """General config settings for flask."""

    PORT = getenv("PORT", 5000)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_ACCESS = ["access", "refresh"]
    BABEL_DEFUALT_LOCALE = getenv("BABEL_DEFUALT_LOCALE")
    BABEL_DEFAULT_TIMEZONE = getenv("BABEL_DEFAULT_TIMEZONE")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://finque_dev:finque_dev@localhost/finque_dev"
    SECRET_KEY = getenv("SECRET_KEY", "my_precious_dev_key")
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", "my_precious_jwt_dev_key")
    SECURITY_PASSWORD_SALT = getenv(
        "SECURITY_PASSWORD_SALT", "146585145368132386173505678016728509634"
    )


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://finque_test:finque_test@localhost/finque_test"
    )
    SECRET_KEY = getenv("SECRET_KEY", "my_precious_testing_key")
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", "my_precious_jwt_testing_key")
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECURITY_PASSWORD_SALT = getenv(
        "SECURITY_PASSWORD_SALT", "146585145368132386173505678016728509635"
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    SECURITY_PASSWORD_SALT = getenv("SECURITY_PASSWORD_SALT")


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
