#!/usr/bin/python3
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '' #key here
    SQLALCHEMY_DATABASE_URI ='' #Postgres url here


class ProductionConfig(Config):
    DEBUG = False
    app.config['APPLICATION_ROOT'] = 'activities.tjhsst.edu/ghs'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
