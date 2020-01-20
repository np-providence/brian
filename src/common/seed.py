#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.feature import add_features
from model.user import add_user
from model.role import add_roles
from model.event import add_event
from model.location import add_location
from loguru import logger
import base64


def seed_user():
    logger.debug('Attempting to seed user')
    data = {
        'email': 'saitama@gmail.com',
        'name': 'Saitama',
        'password': 'password',
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
        "createdBy": "Saitama",
        "dateTimeStart": "Jun 1 2019 1:30PM",
        "dateTimeEnd": "Jun 1 2019 2:30PM",
        "locations": ["IMH", "Graveyard"],
    }
    result = add_event(data)
    if result:
        logger.success('Event Sucessfully added')
    else:
        logger.error('Failed to add event')


def seed_locations():
    logger.debug('Attempting to seed event')
    data = [{'name': 'IMH'}, {'name': 'Graveyard'}]
    for row in data:
        result = add_location(row)
        if result:
            logger.success('{} sucessfully added', row['name'])
        else:
            logger.error('Failed to add {} ', row['name'])
