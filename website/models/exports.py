from lib2to3.pgen2.pgen import generate_grammar
from sqlalchemy import ForeignKey, true
from .people import People
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum, auto
from .campaigns import admins
from datetime import datetime

from flask_login import UserMixin

#Flask WTF
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base

class ExportForm(FlaskForm):
    campaign = SelectField('Campaign:')
    export_type = RadioField('Data to export:', validators=[DataRequired()], choices=['Users', 'Shifts', 'Abstracts', 'Payments', 'Receipts'])
    submit = SubmitField('Submit')

class Exports(db.Model):
    __tablename__ = 'exports'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    # campaign_exported = db.Column(db.Integer, ForeignKey('campaign.id'))
    person_exported = db.Column(db.Integer, ForeignKey('users.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())