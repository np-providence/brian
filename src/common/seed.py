#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.features import add_features
from model.user import add_user
from loguru import logger


def seed_attendee():
    prefix = "data:image/jpeg;base64,"
    string_base64 = None
    with open("../../joebidensides/front.jpeg", "rb") as image_file:
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
        logger.info('Attendee Sucessfully added')
    else:
        logger.info('Failed to add Attendee')


def seed_user():
    data = {
        'email': 'saitama@gmail.com',
        'name': 'Saitama',
        'password': 'password',
        'isAdmin': False
    }
    result = add_user(data)
    if result:
        logger.info('User Sucessfully added')
    logger.info('Failed to add user')
