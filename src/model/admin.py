from marshmallow_sqlalchemy import ModelSchema
from.user import User
from common.common import gen_hash, db

session = db.session

class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.BIGINT(), db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'admin',
    }

class AdminSchema(ModelSchema):
    class Meta:
        model = Admin


