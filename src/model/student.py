import bcrypt
from .user import User 
from common.common import gen_hash, db
from marshmallow_sqlalchemy import ModelSchema

from loguru import logger

session = db.session

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.BIGINT(), db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.BIGINT(), db.ForeignKey('course.id'))
    year_id = db.Column(db.BIGINT(), db.ForeignKey('course.id'))

    __mapper_args__ = {
        'polymorphic_identity':'student',
    }

class StudentSchema(ModelSchema):
    class Meta:
        model = Student

def add_student(data): 
    id = gen_hash()
    new_student = Student(id=id,
                    name=data['name'],
                    email=data['email'],
                    role='student',
                    passHash=bcrypt.hashpw(data['password'].encode('utf-8'),
                                           bcrypt.gensalt()).decode('utf-8'))
    session.add(new_student)
    try: 
        session.commit()
        logger.info('Student user successfully added')
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return id 

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())

class CourseSchema(ModelSchema):
    class Meta:
        model = Course

def add_course(course_name):
    new_course = Course(id=gen_hash(), name=course_name)
    session.add(new_course)
    try: 
        session.commit()
        logger.info('Course successfully added')
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return True 

class Year(db.Model):
    __tablename__ = 'year'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())

class YearSchema(ModelSchema):
    class Meta:
        model = Year

def add_year(year_name):
    new_year = Year(id=gen_hash(), name=year_name)
    session.add(new_year)
    try: 
        session.commit()
        logger.info('Year successfully added')
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return True 


