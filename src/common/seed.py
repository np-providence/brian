#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.features import add_features
from model.attendee import add_attendee
from model.user import add_user, add_roles
from model.event import add_event
from loguru import logger
import base64


def seed_attendee():
    logger.debug('Attempting to seed attendee')
    prefix = "data:image/jpeg;base64,"
    string_base64 = None
    with open("./joebidensides/left.jpeg", "rb") as image_file:
        string_base64 = str(base64.b64encode(image_file.read()), 'utf-8')
    encoded_string = prefix + string_base64
    data = {
        'features': [encoded_string],
        'course': 'Test',
        'year': '2018',
        'gender': 'male',
        'status': True,
        'email': 'test@test.com',
        'password': 'password',
    }
    result = add_attendee(data)
    print("Result ==> ", result)
    if result:
        logger.success('Attendee Sucessfully added')
    else:
        logger.error('Failed to add Attendee')


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
    data = [{'name':'Admin'}, {'name':'User'}]
    for row in data:
        result = add_roles(row)
        if result:
            logger.success('Role Sucessfully added')
        else:
            logger.error('Failed to add Role')


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
