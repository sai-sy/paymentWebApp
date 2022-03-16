from sqlalchemy import true
from .. import db
from datetime import datetime
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired
from sqlalchemy.orm import declarative_base

class LoginForm(FlaskForm):
    email = EmailField('Email Address:', validators=[DataRequired()])
    password = PasswordField()
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email Address:', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password1 = PasswordField('Password')
    password2 = PasswordField('Re-Enter Password')
    submit = SubmitField('Submit')

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return '<Name %r>' % self.name

    __mapper_args__ = {
        'polymorphic_identity':'person',
    }
