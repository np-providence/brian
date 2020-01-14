#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, BIGINT
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from .base import Base, Session
from common.common import session_scope, gen_hash, db

session = Session()


class Event(db.Model):
    __tablename__ = 'Event'
    id = Column(BIGINT, primary_key=True)
    name = Column(String, unique=True)
    sesPerWeek = Column(Integer)
    numOfWeek = Column(Integer)
    location = Column(String)
    createdBy = Column(String)

    def __init__(self, id, name, sesPerWeek, numOfWeek, location, createdBy):
        self.id = id
        self.name = name
        self.sesPerWeek = sesPerWeek
        self.numOfWeek = numOfWeek
        self.location = location
        self.createdBy = createdBy


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
