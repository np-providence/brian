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
        result = []
        attendees = set()
        attendance = list(map(AttendanceSchema().dump, session.query(Attendance).filter_by(event_id=event_id).all()))

        # Build a collection of unique users
        for a in attendance:
            attendees.add(a['user_id'])

        # Get earliest seen time for each attendee
        for attendee in attendees:
            records = list(filter(lambda a: a['user_id'] == attendee, attendance))
            # Sort by date and get earliest seen time
            records = sorted(records, key=lambda x: x['date_time'])
            result.append(records[0])
        return result
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
