#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    #engine = create_engine('postgresql://postgres:mysecretpassword@postgresdb/brian')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

    USER_ENABLE_EMAIL = True  # Enable email authentication
    USER_ENABLE_USERNAME = False
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"

    JWT_SECRET_KEY = os.getenv('SECRET')
