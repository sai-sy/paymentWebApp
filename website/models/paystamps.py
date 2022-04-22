from sqlalchemy import ForeignKey
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired
from datetime import datetime

class PayStampForm(FlaskForm):
    user = SelectField('User: ')
    date = DateField('Date (yyyy/mm/dd): ', validators=[DataRequired()])
    amount = FloatField('Amount: ', validators=[DataRequired()])
    campaign = SelectField('Campaign: ', validators=[DataRequired()])
    activity = SelectField('Activity: ' )
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
    activity_id =db.Column(db.String(500), db.ForeignKey('activities.activity'), default='overall')
    note = db.Column(db.String(500))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return self.first_name + ' ' + self.last_name

    __mapper_args__ = {
        'polymorphic_identity':'paystamp',
    }

