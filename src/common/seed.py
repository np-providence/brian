#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.admin import add_admin 
from model.student import add_student, add_course, add_year
from model.event_owner import add_event_owner
from model.event import add_event
from model.location import add_location
from loguru import logger
import base64


def seed_users():
    logger.debug('Seeding Users...')
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
    if add_event_owner(event_owner) is None:
        logger.error('Could not seed event owner user')


def seed_event():
    logger.debug('Seeding events...')
    data = {
        "name": "Capstone",
        "createdBy": "Saitama",
        "dateTimeStart": "2020-01-20 12:18:23 UTC",
        "dateTimeEnd": "2020-01-20 12:18:23 UTC",
        "locations": ["IMH", "Graveyard"],
    }
    result = add_event(data)
    if result:
        logger.success('Event successfully added')
    else:
        logger.error('Failed to add event')


def seed_locations():
    logger.debug('Seeding Locations...')
    data = [{'name': 'IMH'}, {'name': 'Graveyard'}]
    for row in data:
        result = add_location(row)
        if result:
            logger.success('{} successfully added', row['name'])
        else:
            logger.error('Failed to add {} ', row['name'])

def seed_courses():
    logger.debug('Seeding courses...')
    data = [
            'Information Technology',
            'How I Met Your Mother',
            'Art and design',
            ]
    for row in data:
        if add_course(row) :
            logger.success('{} successfully added', row)
        else:
            logger.error('Failed to add {}', row)

def seed_years():
    logger.debug('Seeding years...')
    data = [
            '2017',
            '2018',
            '2019',
            ]
    for row in data:
        if add_year(row) :
            logger.success('{} successfully added', row)
        else:
            logger.error('Failed to add {}', row)


