#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.feature import add_features
from model.admin import add_admin 
from model.student import add_student 
from model.event_owner import add_event_owner
from model.event import add_event
from model.location import add_location
from loguru import logger
import base64


def seed_users():
    logger.debug('Attempting to seed users...')
    student = {
        'email': 'potatoman50@gmail.com',
        'name': 'Shun Yuan',
        'password': 'password',
    }
    if add_student(student) is None:
        logger.error('Could not seed student')
    admin = {
        'email': 'admin@gmail.com',
        'name': 'Admin',
        'password': 'password',
    }
    if add_admin(admin) is None:
        logger.error('Could not seed admin user')
    event_owner = {
        'email': 'event_owner@gmail.com',
        'name': 'Mr Toh',
        'password': 'password',
    }
    if add_event_owner(admin) is None:
        logger.error('Could not seed event owner user')
    logger.debug('Done seeding.')


def seed_event():
    logger.debug('Attempting to seed event')
    data = {
        "name": "Capstone",
        "createdBy": "Saitama",
        "dateTimeStart": "2020-01-20 12:18:23 UTC",
        "dateTimeEnd": "2020-01-20 12:18:23 UTC",
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
