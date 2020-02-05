from common.common import gen_hash, db
from marshmallow_sqlalchemy import ModelSchema

from loguru import logger

session = db.session

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))
    event_id = db.Column(db.String(), db.ForeignKey('event.id'))
    camera_mac_address = db.Column(db.String())
    date_time = db.Column(db.DateTime())

class AttendanceSchema(ModelSchema):
    class Meta:
        model = Attendance
        include_fk = True

def get_attendance_for_event(event_id):
    try:
        attendance = list(map(AttendanceSchema().dump, session.query(Attendance).filter_by(event_id=event_id).all()))
        return attendance
    except Exception as e:
        logger.error(e)
        raise

def add_attendance(data):
    id = gen_hash()
    new_attendance = Attendance(id=id, 
            user_id=data['user_id'],
            event_id=data['event_id'],
            camera_mac_address=data['camera_mac_address'],
            date_time=data['date_time'])
    session.add(new_attendance)
    try:
        session.commit()
        logger.info('Added attendance record')
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return id
