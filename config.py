from os import path, getenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ""
    ALLOWED_ORIGINS = []


# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
#     ALLOWED_ORIGINS = [getenv("ALLOWED_ORIGINS")]

# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1) if getenv("DATABASE_URL").startswith("postgres://") else getenv("DATABASE_URL")
#     SENTRY_DSN_URI = getenv("SENTRY_DSN_URI")
#     ALLOWED_ORIGINS = [getenv("ALLOWED_ORIGINS")]


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql".join(environ.get("DATABASE_URL").split("postgres"))
    SENTRY_DSN_URI = environ.get("SENTRY_DSN_URI")
    ALLOWED_ORIGINS = [environ.get("ALLOWED_ORIGINS")]
