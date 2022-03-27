from email.policy import default
from lib2to3.pgen2.pgen import generate_grammar
from sqlalchemy import ForeignKey, true
from .people import People
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum, auto
from .campaigns import admins

from flask_login import UserMixin

#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField 
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base

class AdminForm(FlaskForm):
    command = StringField('MYSQL COMMAND:', validators=[DataRequired()])
    message = StringField('Commit Message: ')
    submit = SubmitField('Submit')

class AdminCommands(db.Model):
    __tablename__ = 'admincommands'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    command = db.Column(db.String(1000), nullable=False)
    message = db.Column(db.Text())

class AdminPasswordForm(FlaskForm):
    password = StringField('Admin Access Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdminPassword(db.Model):
    password = db.Column(db.String(150), nullable=False, primary_key=True)