#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.feature import add_features
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


def seed_courses():
    logger.debug('Seeding courses...')
    data = [
        'Information Technology',
        'How I Met Your Mother',
        'Art and design',
    ]
    for row in data:
        if add_course(row):
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
        if add_year(row):
            logger.success('{} successfully added', row)
        else:
            logger.error('Failed to add {}', row)


def seed_eventowner_with_events():
    logger.debug('Seeding event owner with events...')
    event_owner = {
        'email': 'saitama@gmail.com',
        'name': 'saitama',
        'password': 'password',
    }
    try:
        # Add event owner
        event_owner = add_event_owner(event_owner)
        # Get location id [1,2]
        locations = seed_locations()
        # Finally seed event with event_owner id and locations
        result = seed_event(locations, event_owner)
    except Exception as e:
        raise e


def seed_locations():
    logger.debug('Seeding Locations...')
    data = [{'name': 'hdmi'}, {'name': 'cable'}]
    result = []
    for row in data:
        record = add_location(row)
        if record:
            result.append(record)
            logger.success('{} successfully added', row['name'])
        else:
            logger.error('Failed to add {} ', row['name'])
    return result


def seed_event(locations, user):
    logger.debug('Seeding events...')
    data = {
        "name": "Capstone",
        "createdBy": user,
        "dateTimeStart": "2020-01-20 12:18:23 UTC",
        "dateTimeEnd": "2020-01-20 12:18:23 UTC",
        "locations": locations,
    }
    result = add_event(data)
    if result:
        logger.success('{} successfully added', data['name'])
    else:
        logger.error('Failed to add event')
