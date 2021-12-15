import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://pxyerzwuholdqp:e45b07a7306a8868f1ebc5bf3a63d46c8a8416e602f1749c4af90f44ee96140e@ec2-34-204-22-76.compute-1.amazonaws.com: 5432/den4ncj6b3nja4"

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://pxyerzwuholdqp:e45b07a7306a8868f1ebc5bf3a63d46c8a8416e602f1749c4af90f44ee96140e@ec2-34-204-22-76.compute-1.amazonaws.com: 5432/den4ncj6b3nja4"

class LocalConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://brandon:121314121314@localhost/showfeur_development"

class TestingConfig(Config):
    TESTING = True
