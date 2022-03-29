from re import L
from click import command
from flask import Blueprint, jsonify, render_template, request, flash, jsonify, Flask, redirect, url_for, current_app
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from . import db
from .models.users import SystemLevels, Users
from .models.shiftstamps import ShiftStamps, Activities, ShiftStampForm
from .models.admincommands import AdminCommands, AdminForm, AdminPassword, AdminPasswordForm
from .models.campaigns import CampaignForm, Campaigns
views = Blueprint('views', __name__)
import datetime
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from .shift_route import shift_add_func

@views.route('/')
def home():    
    return render_template('home.html')

@views.route('/admin_commands', methods=['GET', 'POST'])
def secret_admin():
    form = AdminForm()
    if form.validate_on_submit():
        commandObj = AdminCommands(
            command=form.command.data,
            message=form.message.data
        )
        with db.engine.connect() as connection:
            result = connection.execute(text(form.command.data  ))
            flash(result)
        db.session.add(commandObj)
        db.session.commit()

        return render_template('admin_command.html', form=form)
    else:
        flash('Wrong Password')

    return render_template('admin_command.html', form=form)

@views.route('/admin_commands_closed', methods=['GET', 'POST'])
def secret_admin_closed():
    passForm = AdminPasswordForm()
    form = AdminForm()
    if passForm.validate_on_submit():
        password = AdminPassword.query.first() 
        if check_password_hash(password.password, passForm.password.data):
            if form.validate_on_submit():
                commandObj = AdminCommands(
                    command=form.command.data,
                    message=form.message.data
                )
                with db.engine.connect() as connection:
                    result = connection.execute(text(form.command.data  ))
                    flash(result)
                db.session.add(commandObj)
                db.session.commit()

                return render_template('admin_command.html', form=form)

            return render_template('admin_command.html', form=form)
        else:
            flash('Wrong Password')

    return render_template('admin_command.html', form=form)
        

@views.route('/user/<name>')
@login_required
def user(name):
    return render_template('user.html', user_name=name)

@views.route('/user_list')
@login_required
def user_list():
    our_users_grabbed = Users.query.order_by(Users.date_added)
    return render_template('/user/user_list.html', our_users=our_users_grabbed)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def user_home():
    return redirect(url_for('shift_route.shift_add'))

@views.route('/user/profile/<id>')
@login_required
def profile(id):
    if str(current_user.id) != id:
        current_app.logger.info(current_user.id==str(id))
        return render_template('no_access.html')
    else:
        return render_template('/user/profile.html', id=id)

@views.app_errorhandler(404)
def page_not_found(e):
    '''Invalid URL'''
    return render_template("404.html"), 404

@views.app_errorhandler(500)
def internal_server_error(e):
    '''Internal Server Error'''
    return render_template("500.html"), 500

@views.app_errorhandler(403)
def internal_server_error(e):
    '''Internal Server Error'''
    return render_template("403.html"), 403

