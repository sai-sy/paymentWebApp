from email.policy import default
from sqlalchemy import Column, ForeignKey, true
from paymentWebApp.website.models.paystamps import PayStamps
from paymentWebApp.website.models.receipts import Receipts

from paymentWebApp.website.models.shiftstamps import ShiftStamps
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, IntegerField, SelectMultipleField, FloatField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base
from datetime import datetime

from functools import reduce

from ..models.abstracts import AbstractStamps

class GovLevels(db.Model):
    __tablename__ = 'govlevels'
    level = db.Column(db.String(50), nullable=False, primary_key=true)
    campaigns = db.relationship('Campaigns', back_populates='gov_level')

class CreateCampaignForm(FlaskForm):
    candidate = StringField('Candidate', validators=[DataRequired()])
    alias = StringField('Internal Reference Name (firstName_year):', validators=[DataRequired()])
    riding = StringField('Riding:', validators=[DataRequired()])
    year = IntegerField('Election Year:', validators=[DataRequired()])
    gov_level = SelectField('Gov Level:', validators=[DataRequired()])
    hourly_rate = FloatField('Hourly Value:')
    submit = SubmitField('Submit')

class JoinCampaignForm(FlaskForm):
    hex_code=StringField('Enter the provided code for your campaign')
    submit = SubmitField('Submit')

class CampaignContractForm(FlaskForm):
    user = SelectField('User:')
    campaign = SelectField('Campaign:')
    getting_paid = BooleanField('Getting Paid?')
    getting_commute_pay = BooleanField('Getting Commute Pay?')
    admin_rate = FloatField('Admin Hourly Rate:', validators=[DataRequired()])
    canvass_rate = FloatField('Canvass Hourly Rate:', validators=[DataRequired()])
    calling_rate = FloatField('Calling Hourly Rate:', validators=[DataRequired()])
    general_rate = FloatField('General Hourly Rate:', validators=[DataRequired()])
    litdrop_rate = FloatField('Litdrop Hourly Rate:', validators=[DataRequired()])
    commute_rate = FloatField('Commute Hourly Rate:', validators=[DataRequired()])
    submit = SubmitField('Submit')

admins = db.Table('admins', db.Model.metadata, 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')), 
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id'))
)

payment_exceptions = db.Table('payment_exceptions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id')),
    db.Column('hourly_rate', db.Integer)
)

default_pay_rates = {
    'admin_rate' : '15.0',
    'canvass_rate' : '15.0',
    'calling_rate' : '15.0',
    'general_rate' : '15.0',
    'litdrop_rate' : '15.0',
    'commute_rate' : '6.50'
}

class Pay_Per_Users(db.Model):
    __tablename__ = 'pay_output'
    user_id = db.Column(db.Intger, db.ForeignKey('users.id'))
    user  = db.relationship('Users', back_populates='pay_from_campaigns')
    campaign_id = db.Column(db.Intger, db.ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaigns', back_populates='pay_per_user')
    pay_sum = db.Column(db.JSON)


class Campaign_Contracts(db.Model):
    __tablename__ = 'campaign_contracts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id')) 
    campaign_id = db.Column(db.ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaigns', back_populates='user_contracts')
    user = db.relationship("Users", back_populates='campaign_contracts')
    getting_paid = db.Column(db.Boolean, default=False)
    getting_commute_pay = db.Column(db.Boolean, default=False)
    pay_rates = db.Column(db.JSON, nullable=False, default=default_pay_rates)

class Campaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #if this gets uncommented, make sure to uncomment Users.py candidacies
    #candidate_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    #candidate = db.relationship('Users', back_populates="candidacies")
    
    # Campaign Info
    candidate = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(50), nullable=False)
    riding = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    gov_level_id = db.Column(db.String(50), db.ForeignKey('govlevels.level'), nullable=False)
    gov_level = db.relationship('GovLevels')
    
    # Management Info
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('Users', back_populates='campaigns_owned')
    admins = db.relationship('Users', secondary=admins, back_populates="admin_campaigns")
    user_contracts = db.relationship('Campaign_Contracts', back_populates="campaign")
    
    # Stamps
    shiftstamps_on_campaign = db.relationship('ShiftStamps', back_populates='campaign')
    paystamps_on_campaign = db.relationship('PayStamps', back_populates='campaign')
    abstractstamps_on_campaign = db.relationship('AbstractStamps', back_populates='campaign')
    receipts = db.relationship('Receipts', back_populates='campaign')
    
    hex_code = db.Column(db.String(30), nullable=False, unique=True)
    
    # Pay Amount
    commute_pay = db.Column(db.Float, nullable=False, default=0)
    pay_rates = db.Column(db.JSON, nullable=False, default=default_pay_rates)
    admin_rate = db.Column(db.Float, nullable=False, default=15.0)
    canvass_rate = db.Column(db.Float, nullable=False, default=15.0)
    calling_rate = db.Column(db.Float, nullable=False, default=15.0)
    general_rate = db.Column(db.Float, nullable=False, default=15.0)
    litdrop_rate = db.Column(db.Float, nullable=False, default=15.0)
    pay_per_user = db.relationship("Pay_Per_Users", back_populates='campaign')

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

    def process_pay(self):
        '''Process the pay in a Pay_Per_Users object
        user_id: int
        user: relationship
        campaign_id: int
        campaign: relationship
        pay_sum = {
            shift_based: {
                each_activity: float
                total: int
            },
            receipts_total: float,
            abstracts_total: float,
            total_earned: float,
            paystamps_total: {
                each_activity: float,
                no_category: float
                total: float
            },
            owed = {
                each_activity: float
                all_activites: float
                total: float
            }
        }
        '''
        out = {}
        shift_based = {}
        receipts_abstracts = {}
        paystamps = {}

        # Iterate every contract
        user_contract: Campaign_Contracts
        for user_contract in self.user_contracts:
            total = 0
            
            # Calculate every shift based earning
            for pay_rate, pay_rate_amount in user_contract.pay_rates.items():
                shifts = ShiftStamps.query.filter_by(user_id=user_contract.user_id, activity=str(pay_rate).replace('_rate', ''))
                shift_total = 0
                shift: ShiftStamps
                for shift in shifts:
                    shift_total = shift_total + (shift.minutes * (pay_rate_amount/60))

                shift_based[str(pay_rate).replace('_rate', '')] = shift_total

            total = 0
            for total_values in shift_based.values():
                total += total_values

            shift_based['total'] = total

            total = 0

            # Receipts and Abstracts
            receipts_abstracts['receipts'] = 0
            receipts = Receipts.query.filter_by(user_id=user_contract.user_id)
            r: Receipts
            for r in receipts:
                receipts_abstracts['receipts'] += r.amount

            receipts_abstracts['abstracts'] = 0
            abstracts = AbstractStamps.query.filter_by(user_id=user_contract.user_id)
            r: AbstractStamps
            for r in abstracts:
                receipts_abstracts['abstracts'] += r.amount

            # Paystamps
            for pay_rate, pay_rate_amount in user_contract.pay_rates.items():
                paystamp_arr = PayStamps.query.filter_by(user_id=user_contract.user_id, description=str(pay_rate).replace('_rate', ''))
                total_paid = 0
                paystamp_item: PayStamps
                for paystamp_item in paystamp_arr:
                    total_paid =+ paystamp_item.amount

                paystamps[str(pay_rate).replace('_rate', '')] = total_paid

            total = 0
            for total_values in shift_based.values():
                total += total_values

            

            #Output
            out['shift_based'] = shift_based
            out.update(receipts_abstracts)
            out['paystamps'] = paystamps
