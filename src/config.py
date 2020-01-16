#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@postgresdb/brian'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

    JWT_SECRET_KEY = os.getenv('SECRET')
