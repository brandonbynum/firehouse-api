from os import environ, path

basedir = path.abspath(path.dirname(__file__))

database_url = "postgresql".join(environ.get("DATABASE_URL").split("postgres"))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ""
    ALLOWED_ORIGINS = []


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = database_url
    ALLOWED_ORIGINS = [environ.get("ALLOWED_ORIGINS")]
    SENTRY_DSN_URI = environ.get("SENTRY_DSN_URI")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = database_url
    SENTRY_DSN_URI = environ.get("SENTRY_DSN_URI")
    ALLOWED_ORIGINS = [environ.get("ALLOWED_ORIGINS")]
