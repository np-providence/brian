from.user import User
from common.common import gen_hash, db

session = db.session

class EventOwner(User):
    __tablename__ = 'event_owner'
    id = db.Column(db.BIGINT(), db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'event_owner',
    }


