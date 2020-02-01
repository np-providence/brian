#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.admin import add_admin
from model.student import add_student, add_course, add_year
from model.event_owner import add_event_owner
from model.event import add_event
from model.location import add_location
from loguru import logger
import base64

def seed_all():
    courses = seed_courses()
    years = seed_years()
    locations = seed_locations()

    if len(courses) > 0 and len(years) > 0:
        users = seed_users(courses, years)
        if len(users) > 0  and len(locations) > 0: 
            events = seed_events(users[2], locations)
    

def seed_users(courses, years):
    logger.debug('Seeding Users...')
    student = {
        'email': 'potatoman50@gmail.com',
        'name': 'Shun Yuan',
        'password': 'password',
        'course_id': courses[0],
        'year_id': years[0] 
    }
    student_id = add_student(student)
    if student_id is None:
        logger.error('Could not seed student')
    admin = {
        'email': 'admin@gmail.com',
        'name': 'Admin',
        'password': 'password',
    }
    admin_id = add_admin(admin)
    if admin_id is None:
        logger.error('Could not seed admin user')
    event_owner = {
        'email': 'event_owner@gmail.com',
        'name': 'Mr Toh',
        'password': 'password',
    }
    event_owner_id = add_event_owner(event_owner)
    if event_owner_id is None:
        logger.error('Could not seed event owner user')
    return [student_id, admin_id, event_owner_id]


def seed_courses():
    logger.debug('Seeding courses...')
    data = [
        'Information Technology',
        'How I Met Your Mother',
        'Art and design',
    ]
    course_ids = []
    for row in data:
        try:
            course_ids.append(add_course(row))
            logger.success('{} successfully added', row)
        except Exception as e:
            logger.error(e)
    return course_ids


def seed_years():
    logger.debug('Seeding years...')
    data = [
        '2017',
        '2018',
        '2019',
    ]
    year_ids = []
    for row in data:
        try: 
            year_ids.append(add_year(row))
            logger.success('{} successfully added', row)
        except Exception as e:
            logger.error(e)
    return year_ids

def seed_locations():
    logger.debug('Seeding Locations...')
    data = [{'name': 'hdmi'}, {'name': 'cable'}]
    location_ids = []
    for row in data:
        record = add_location(row)
        if record:
            location_ids.append(record)
            logger.success('{} successfully added', row['name'])
        else:
            logger.error('Failed to add {} ', row['name'])
    return location_ids 


def seed_events(event_owner_id, locations):
    logger.debug('Seeding events...')
    data = {
        "name": "Capstone",
        "createdBy": event_owner_id,
        "dateTimeStart": "2020-01-20 12:18:23 UTC",
        "dateTimeEnd": "2020-01-20 12:18:23 UTC",
        "locations": locations,
    }
    result = add_event(data)
    if result:
        logger.success('{} successfully added', data['name'])
    else:
        logger.error('Failed to add event')
