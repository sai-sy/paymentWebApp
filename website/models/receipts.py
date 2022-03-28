from pymysql import Date
from sqlalchemy import true, Table, ForeignKey
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, DateField, TimeField, FloatField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base
from datetime import datetime

from ..helper_functions.timeresponse import listoftimes

class ReceiptForm(FlaskForm):
    users = SelectField('User: ', validators=[DataRequired()])
    date = DateField('Date: ', validators=[DataRequired()])
    amount = FloatField('Amount: ', validators=[DataRequired()])
    campaigns = SelectField('Campaign: ', validators=[DataRequired()])
    image = FileField('Upload Image: ', validators=[FileRequired()])
    submit = SubmitField('Submit')

class Receipts(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship('Users', back_populates='receipts')
    campaign_id = db.Column(db.Integer, ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaigns', back_populates='receipts')
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    image_name = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    
    __mapper_args__ = {
        'polymorphic_identity':'receipt',
    }
