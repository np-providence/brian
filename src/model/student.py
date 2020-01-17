from.user import User
from common.common import gen_hash, db

session = db.session

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.BIGINT(), db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.BIGINT(), db.ForeignKey('course.id'))
    year_id = db.Column(db.BIGINT(), db.ForeignKey('course.id'))

    __mapper_args__ = {
        'polymorphic_identity':'student',
    }

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())

class Year(db.Model):
    __tablename__ = 'year'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())

