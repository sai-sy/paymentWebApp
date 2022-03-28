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
    form = ShiftStampForm()
    choiceMath = [(Users.query.get_or_404(current_user.id).id, str(Users.query.get_or_404(current_user.id).first_name) + ' ' + str(Users.query.get_or_404(current_user.id).last_name))]
    form.user.choices = choiceMath
    form.activity.choices = [str(a.activity) for a in Activities.query.order_by()]
    form.campaign.choices = [(str(c.id), str(c.alias))  for c in Campaigns.query.order_by()]
    if form.validate_on_submit():

        calcedStart = datetime.datetime.combine(form.date.data, datetime.datetime.strptime(form.start_time.data, '%H:%M:%S').time())
        comparedShift = ShiftStamps.query.filter_by(user_id=form.user.data, start_time=calcedStart).first()
        if comparedShift:
            flash("This Shift Already Exists.", category='error')
        else:
            founduser = Users.query.filter_by(id=form.user.data).first()
            foundactivity = Activities.query.filter_by(activity=form.activity.data).first()
            shiftstamp = ShiftStamps(user_id=founduser.id, start_time=calcedStart,
                end_time=datetime.datetime.combine(form.date.data, datetime.datetime.strptime(form.end_time.data, '%H:%M:%S').time()),
                activity_id=form.activity.data,
                activity=foundactivity,
                campaign_id=form.campaign.data
            )
            shiftstamp.minutes = (shiftstamp.end_time - shiftstamp.start_time).total_seconds() / 60
            db.session.add(shiftstamp)
            db.session.commit()

            form.user.data = ''
            form.date.data = ''
            form.start_time.data = ''
            form.end_time.data = ''
            form.activity.data = ''
            flash("Shift Added Successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template('/shift/shift_add.html', form=form)

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

