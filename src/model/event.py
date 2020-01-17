#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, BIGINT
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import gen_hash, db

from model.location import Location

session = db.session


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())
    created_by = db.Column(String())
    date_time_start = db.Column(db.DateTime())
    date_time_end = db.Column(db.DateTime())
    locations = db.relationship('Location',
                                secondary='event_location',
                                backref=db.backref('event', lazy='joined'))


class EventLocation(db.Model):
    __tablename__ = 'event_location'
    id = db.Column(db.BIGINT(), primary_key=True)
    event_id = db.Column(db.BIGINT(),
                         db.ForeignKey('event.id', ondelete='CASCADE'))
    location_id = db.Column(db.Integer(),
                            db.ForeignKey('location.id', ondelete='CASCADE'))


class EventSchema(ModelSchema):
    class Meta:
        model = Event


def add_event(data):
    didSucceed = False
    hash_id = gen_hash()
    new_event = Event(id=hash_id,
                      name=data['name'],
                      sesPerWeek=data['sessionPerWeek'],
                      numOfWeek=data['numberOfWeeks'],
                      location=data['location'],
                      createdBy=data['createdBy'])
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
        event = session.query(Event).filter_by(name=name).first()
        return event
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
