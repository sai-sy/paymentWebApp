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
from wtforms import StringField, SubmitField, PasswordField, EmailField, RadioField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy.orm import declarative_base

class ImportForm(FlaskForm):
    import_type = RadioField('What Are You Importing:', validators=[DataRequired()], choices=['Shifts', 'Payments', 'Users', 'Abstracts'])
    file = FileField('Upload Spreadsheet: ', validators=[FileRequired()])
    submit = SubmitField('Submit')

class Imports(db.Model):
    __tablename__ = 'imports'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    file_name = db.Column(db.String(1000), nullable=False)
    person_imported = db.Column(db.Integer, ForeignKey('users.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())