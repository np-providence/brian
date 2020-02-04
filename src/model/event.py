#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import Nested
from loguru import logger
from datetime import datetime

from common.common import gen_hash, db

from model.location import Location, LocationSchema

session = db.session


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.String(), primary_key=True)
    created_by = db.Column(db.String(),
                           db.ForeignKey('user.id', ondelete='CASCADE'))
    name = db.Column(db.String())
    date_time_start = db.Column(db.DateTime())
    date_time_end = db.Column(db.DateTime())
    locations = db.relationship('Location',
                                secondary='event_location',
                                lazy='select',
                                backref=db.backref('event', lazy='joined'))


class EventLocation(db.Model):
    __tablename__ = 'event_location'
    event_id = db.Column(db.String(),
                         db.ForeignKey('event.id', ondelete='CASCADE'),
                         primary_key=True)
    location_id = db.Column(db.String(),
                            db.ForeignKey('location.id', ondelete='CASCADE'),
                            primary_key=True)


class EventSchema(ModelSchema):
    locations = Nested(LocationSchema, many=True)

    class Meta:
        model = Event
        include_fk = True


class EventLocationSchema(ModelSchema):
    class Meta:
        model = EventLocation

event_schema = EventSchema()
event_location_schema = EventLocationSchema(many=True)


def add_event(data):
    id = gen_hash()
    new_event = Event(id=id,
                      name=data['name'],
                      created_by=data['createdBy'],
                      date_time_start=data['dateTimeStart'],
                      date_time_end=data['dateTimeEnd'])

    location_arr = [
        session.query(Location).filter_by(id=location).first()
        for location in data['locations']
    ]
    new_event.locations = location_arr
    session.add(new_event)
    logger.info('Attempting to add event')
    try:
        session.commit()
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return id 


def get_event(name):
    logger.info("Attempting to get event")
    try:
        events = session.query(Event).filter_by(name=name).all()
        for row in events:
            print(event_schema.dump(row))
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
