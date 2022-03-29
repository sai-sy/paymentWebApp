from typing import Text
from sqlalchemy import ForeignKey
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

from ..helper_functions.timeresponse import listoftimes

class AbstractForm(FlaskForm):
    user = SelectField('User: ')
    campaign = SelectField('Campaign: ', validators=[DataRequired()])
    amount = FloatField('Amount: ')
    notes = TextAreaField('Notes: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AbstractStamps(db.Model):
    __tablename__ = 'abstractstamps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship('Users', back_populates='abstractstamps')
    campaign_id = db.Column(db.Integer, ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaigns', back_populates='abstractstamps_on_campaign')
    amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return self.first_name + ' ' + self.last_name

    __mapper_args__ = {
        'polymorphic_identity':'abstract',
    }

