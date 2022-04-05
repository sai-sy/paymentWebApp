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

class LoginForm(FlaskForm):
    email = EmailField('Email Address:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),])
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email Address:', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords Must Match!')])
    password2 = PasswordField('Re-Enter Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SystemLevels(db.Model):
    __tablename__ = 'systemlevels'
    numeric_level = db.Column(db.Integer, nullable=False, primary_key=True)
    level = db.Column(db.String(50), nullable=False)
    users = db.relationship('Users', back_populates='system_level')

class Users(People, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, ForeignKey('people.id'), primary_key=True)
    #password = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    system_level_id = db.Column(db.Integer, ForeignKey('systemlevels.numeric_level'), nullable=False,  default='1')
    system_level = db.relationship('SystemLevels', back_populates='users')
    #make sure to uncoment Campaigns along with this
    #candidacies = db.relationship('Campaigns', back_populates="candidate")
    admin_campaigns = db.relationship('Campaigns', secondary=admins, back_populates="admins")
    campaigns_under = db.relationship('Campaigns', secondary=admins, back_populates="users_under")
    campaigns_owned = db.relationship('Campaigns', back_populates='owner')
    shiftstamps = db.relationship('ShiftStamps', back_populates="user")
    paystamps = db.relationship('PayStamps', back_populates="user")
    abstractstamps = db.relationship('AbstractStamps', back_populates="user")
    receipts = db.relationship('Receipts', back_populates="user")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, "sha256")

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    __mapper_args__ = {
        'polymorphic_identity':'users',
    }