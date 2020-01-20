#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from loguru import logger
from datetime import datetime

from common.common import gen_hash, db

from model.location import Location, LocationSchema

session = db.session


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())
    created_by = db.Column(db.String())
    date_time_start = db.Column(db.DateTime())
    date_time_end = db.Column(db.DateTime())
    locations = db.relationship('Location',
                                secondary='event_location',
                                lazy='select',
                                backref=db.backref('event', lazy='joined'))


class EventLocation(db.Model):
    __tablename__ = 'event_location'
    event_id = db.Column(db.BIGINT(),
                         db.ForeignKey('event.id', ondelete='CASCADE'),
                         primary_key=True)
    location_id = db.Column(db.Integer(),
                            db.ForeignKey('location.id', ondelete='CASCADE'),
                            primary_key=True)


class EventSchema(ModelSchema):
    class Meta:
        model = Event


class EventLocationSchema(ModelSchema):
    class Meta:
        model = EventLocation


event_schema = EventSchema()
event_location_schema = EventLocationSchema(many=True)


def add_event(data):
    didSucceed = False
    hash_id = gen_hash()
    dateTimeStart = datetime.strptime(data['dateTimeStart'],
                                      '%b %d %Y %I:%M%p')
    dateTimeEnd = datetime.strptime(data['dateTimeEnd'], '%b %d %Y %I:%M%p')
    new_event = Event(id=hash_id,
                      name=data['name'],
                      created_by=data['createdBy'],
                      date_time_start=dateTimeStart,
                      date_time_end=dateTimeEnd)

    location_arr = [
        session.query(Location).filter_by(name=location).first()
        for location in data['locations']
    ]
    new_event.locations = location_arr
    session.add(new_event)
    logger.info('Attempting to add event')
    try:
        session.commit()
        didSucceed = True
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_event(name):
    logger.info("Attempting to get event")
    try:
        events = session.query(Event).filter_by(name=name).all()
        return events
    except Exception as e:
        print(e)


def get_events_by_user(user):
    logger.info("Attempting to get list of user created event")
    try:
        event = session.query(Event).filter_by(createdBy=user).first()
        return event
    except Exception as e:
        print(e)


def get_all_event():
    logger.info("Attempting to get all event")
    try:
        event = session.query(Event).all()
        return event
    except Exception as e:
        print(e)
