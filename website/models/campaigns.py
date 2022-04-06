from sqlalchemy import Column, ForeignKey, true
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, IntegerField, SelectMultipleField, FloatField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base
from datetime import datetime

gov_levels = [("1", 'Municipal'), ('2', 'Provincial'), ('3', 'Federal')]

def get_value_label_gov():
    arr = []
    for value, label in enumerate(GovLevels):
        arr.append((value, str(label).strip('GovLevels.')))

class GovLevels(db.Model):
    level = db.Column(db.String(50), nullable=False, primary_key=true)

class CampaignForm(FlaskForm):
    candidate = StringField('Candidate', validators=[DataRequired()])
    alias = StringField('Internal Reference Name (firstName_year):', validators=[DataRequired()])
    riding = StringField('Riding:', validators=[DataRequired()])
    year = IntegerField('Election Year:', validators=[DataRequired()])
    gov_level = SelectField('Gov Level:', validators=[DataRequired()], choices=gov_levels)
    hourly_rate = FloatField('Hourly Value:')
    admins = SelectMultipleField('Admins (Ctl + Click to select multiple):')
    submit = SubmitField('Submit')

class JoinCampaignForm(FlaskForm):
    hex_code=StringField('Enter the provided code for your campaign')
    submit = SubmitField('Submit')

admins = db.Table('admins', db.Model.metadata, 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')), 
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id'))
)

users_under_campaign = db.Table('users_under_campaign', db.Model.metadata, 
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
    gov_level = db.Column(db.String(50), nullable=False)
    pay = db.Column(db.Float, nullable=False, default=15.0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('Users', back_populates='campaigns_owned')
    admins = db.relationship('Users', secondary=admins, back_populates="admin_campaigns")
    users_under = db.relationship('Users', secondary=users_under_campaign, back_populates="campaigns_under")
    shiftstamps_on_campaign = db.relationship('ShiftStamps', back_populates='campaign')
    paystamps_on_campaign = db.relationship('PayStamps', back_populates='campaign')
    abstractstamps_on_campaign = db.relationship('AbstractStamps', back_populates='campaign')
    receipts = db.relationship('Receipts', back_populates='campaign')
    hex_code = db.Column(db.String(30), nullable=False, unique=True)
    hourly_rate = db.Column(db.Float, nullable=False, default=15.0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, **kwargs):
        super(Campaigns, self).__init__(**kwargs)
        for user in self.admins:
            user.system_level_id = 4

        db.session.commit()

    def upgrade_to_admin(self):
        for user in self.admins:
            user.system_level_id = 4

        db.session.commit()
    
    import random