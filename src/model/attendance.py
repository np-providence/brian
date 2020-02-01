from common.common import gen_hash, db
from marshmallow_sqlalchemy import ModelSchema

session = db.session

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.BIGINT(), db.foreignKey('user.id'))
    event_id = db.Column(db.BIGINT(), db.foreignKey('event.id'))
    camera_mac_address = db.Column(db.String())
    date_time = db.Column(db.DateTime())

class AttendanceSchema(ModelSchema):
    class Meta:
        model = Attendance


