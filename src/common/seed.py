#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.features import add_features
from model.user import add_user
from model.role import add_roles
from model.event import add_event
from loguru import logger
import base64


def seed_user():
    logger.debug('Attempting to seed user')
    data = {
        'email': 'saitama@gmail.com',
        'name': 'Saitama',
        'password': 'password',
        'isAdmin': True
    }
    result = add_user(data)
    if result:
        logger.success('User Sucessfully added')
    else:
        logger.error('Failed to add user')


def seed_roles():
    data = [{'name': 'Admin'}, {'name': 'User'}]
    for row in data:
        result = add_roles(row)
        if result:
            logger.success('{} role ucessfully added', row['name'])
        else:
            logger.error('Failed to add {} role', row['name'])


def seed_event():
    logger.debug('Attempting to seed event')
    data = {
        "name": "Capstone",
        "sessionPerWeek": 2,
        "numberOfWeeks": 9,
        "location": "IMH",
        "createdBy": "Saitama"
    }
    result = add_event(data)
    if result:
        logger.success('Event Sucessfully added')
    else:
        logger.error('Failed to add event')
