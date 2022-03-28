from sqlalchemy import true, Table, ForeignKey
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, DateField, TimeField, FloatField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base
from datetime import datetime

from ..helper_functions.timeresponse import listoftimes

class PayStampForm(FlaskForm):
    user = SelectField('User: ')
    date = DateField('Date (yyyy/mm/dd): ', validators=[DataRequired()])
    amount = FloatField('Amount: ', validators=[DataRequired()])
    campaign = SelectField('Campaign: ', validators=[DataRequired()])
    activity = SelectField('Activity: ' )
    notes = StringField('Notes: ')
    submit = SubmitField('Submit')

class PayStamps(db.Model):
    __tablename__ = 'paystamps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship('Users', back_populates='paystamps')
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    campaign_id = db.Column(db.Integer, ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaigns', back_populates='paystamps_on_campaign')
    activity_id = db.Column(db.String(50), ForeignKey('activities.activity'))
    activity = db.relationship("Activities", back_populates='paystamps')
    notes = db.column(db.String(1000))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return self.first_name + ' ' + self.last_name

    __mapper_args__ = {
        'polymorphic_identity':'paystamp',
    }

