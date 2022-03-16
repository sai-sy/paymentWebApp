from sqlalchemy import ForeignKey, true
from .person import People
from .. import db
import datetime

class Users(People):
    __tablename__ = 'users'
    id = db.Column(db.Integer, ForeignKey('people.id'), primary_key=True)
    password = db.Column(db.String(150), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'users',
    }