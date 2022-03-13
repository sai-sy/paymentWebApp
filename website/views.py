from flask import Blueprint, jsonify, render_template, request, flash, jsonify
from flask_login import login_required, logout_user, current_user
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

