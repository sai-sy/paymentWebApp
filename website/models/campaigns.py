from email.policy import default
import enum
from statistics import variance
from sqlalchemy import Column, ForeignKey, true
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base
from datetime import datetime

from enum import Enum, auto

class GovLevels(Enum):
    Munical = auto()
    Provincial = auto()
    Federal = auto()

gov_levels = [("1", 'Munipal'), ('2', 'Provincial'), ('3', 'Federal')]

def get_value_label_gov():
    arr = []
    for value, label in enumerate(GovLevels):
        arr.append((value, str(label).strip('GovLevels.')))


class CampaignForm(FlaskForm):
    candidate = StringField('Candidate', validators=[DataRequired()])
    alias = StringField('Internal Reference Name (firstName_year):', validators=[DataRequired()])
    riding = StringField('Riding:', validators=[DataRequired()])
    year = IntegerField('Election Year:', validators=[DataRequired()])
    gov_level = SelectField('Gov Level:', validators=[DataRequired()], choices=gov_levels)
    admins = SelectMultipleField('Admins:')
    submit = SubmitField('Submit')

admins = db.Table('admins', db.Model.metadata, 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')), 
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id'))
)

class Campaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #if this gets uncommented, make sure to uncomment Users.py candidacies
    #candidate_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    #candidate = db.relationship('Users', back_populates="candidacies")
    candidate = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(50), nullable=False)
    riding = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    gov_level = db.Column(db.String(200), nullable=False)
    pay = db.Column(db.Float, nullable=False, default=15.0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('Users', back_populates='campaigns_owned')
    admins = db.relationship('Users', secondary=admins, back_populates="admin_campaigns")
    shiftstamps_on_campaign = db.relationship('ShiftStamps', back_populates='campaign')
    receipts = db.relationship('Receipts', back_populates='campaign')
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    