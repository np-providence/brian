import bcrypt
from .user import User
from common.common import gen_hash, db
from marshmallow_sqlalchemy import ModelSchema

from loguru import logger

session = db.session


class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.String(), db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.String(), db.ForeignKey('course.id'))
    year_id = db.Column(db.String(), db.ForeignKey('year.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }


class StudentSchema(ModelSchema):
    class Meta:
        model = Student
        include_fk = True


def add_student(data):
    id = gen_hash()
    new_student = Student(id=id,
                    name=data['name'],
                    email=data['email'],
                    course_id= data['course_id'],
                    year_id= data['year_id'],
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

def get_students():
    try:
        results = Student.query.all()
        results = list(map(lambda x: StudentSchema().dump(x), results))
        for student in results:
            del student['passHash']
            del student['role']
        return results
    except Exception as e:
        logger.error(e)
        raise

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), unique=True)


class CourseSchema(ModelSchema):
    class Meta:
        model = Course


def add_course(course_name):
    id = gen_hash()
    new_course = Course(id=id, name=course_name)
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
        return id 

def get_courses():
    try:
        results = Course.query.all()
        results = list(map(lambda x: CourseSchema().dump(x), results))
        logger.info(results)
        return results
    except Exception as e:
        logger.error(e)
        raise

class Year(db.Model):
    __tablename__ = 'year'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), unique=True)


class YearSchema(ModelSchema):
    class Meta:
        model = Year


def add_year(year_name):
    id = gen_hash()
    new_year = Year(id=id, name=year_name)
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
        return id 

def get_years():
    try:
        results = Year.query.all()
        results = list(map(lambda x: YearSchema().dump(x), results))
        return results
    except Exception as e:
        logger.error(e)
        raise
