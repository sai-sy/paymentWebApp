from email.policy import default
from sqlalchemy import ForeignKey
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from datetime import datetime

from ..helper_functions.timeresponse import listoftimes

class ShiftStampForm(FlaskForm):
    user = SelectField('User: ')
    date = DateField('Date (yyyy/mm/dd): ', validators=[DataRequired()])
    start_time = SelectField('Start Time: ', validators=[DataRequired()], choices=listoftimes())
    end_time = SelectField('End Time: ', validators=[DataRequired()], choices=listoftimes())
    campaign = SelectField('Campaign: ', validators=[DataRequired()])
    activity = SelectField('Activity: ' )
    submit = SubmitField('Submit')

class Activities(db.Model):
    __tablename__ = 'activities'
    activity = db.Column(db.String(50), nullable=False, primary_key=True)
    shiftstamps = db.relationship("ShiftStamps", back_populates="activity")

class ShiftStamps(db.Model):
    __tablename__ = 'shiftstamps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship('Users', back_populates='shiftstamps')
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    minutes= db.Column(db.Integer, nullable=False)
    campaign_id = db.Column(db.Integer, ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaigns', back_populates='shiftstamps_on_campaign')
    #campaign = db.relationship('Campaigns')
    activity_id = db.Column(db.String(50), ForeignKey('activities.activity'))
    activity = db.relationship("Activities", back_populates='shiftstamps')
    hourly_rate = db.Column(db.Float, nullable=False, default=15.0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return self.first_name + ' ' + self.last_name

    __mapper_args__ = {
        'polymorphic_identity':'shiftstamp',
    }

