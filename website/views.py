from flask import Blueprint, jsonify, render_template, request, flash, jsonify, Flask
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from . import db
from .models.user import Users
views = Blueprint('views', __name__)

@views.route('/')
def home():
    our_users = Users.query.order_by(Users.date_added)
    return render_template('home.html', our_users=our_users)

@views.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)


@views.app_errorhandler(404)
def page_not_found(e):
    '''Invalid URL'''
    return render_template("404.html"), 404

@views.app_errorhandler(500)
def internal_server_error(e):
    '''Internal Server Error'''
    return render_template("500.html"), 500

