from secrets import choice
from flask import Blueprint, jsonify, redirect, render_template, request, flash, jsonify, Flask, url_for
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy import alias, insert
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from . import db
from .models.users import Users
from .models.people import People
from .models.shiftstamp import ShiftStampForm, ShiftStamps, Activities
from datetime import datetime
shift_route = Blueprint('shift_route', __name__)

@shift_route.route('/shift_add', methods=['GET', 'POST'])
def shift_add():
    form = ShiftStampForm()
    choiceMath = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
    form.user.choices = choiceMath
    form.activity.choices = [str(a.activity) for a in Activities.query.order_by()]
    if form.validate_on_submit():
        
        founduser = Users.query.filter_by(id=form.user.data).first()
        shiftstamp = ShiftStamps(user_id=founduser.id, start_time=datetime.combine(form.date.data, datetime.strptime(form.start_time.data, '%H:%M:%S').time()),
            end_time=datetime.combine(form.date.data, datetime.strptime(form.end_time.data, '%H:%M:%S').time()),
            activity=form.activity.data
            )
        shiftstamp.minutes = shiftstamp.end_time - shiftstamp.start_time.total_seconds() / 60
        comparedShift = ShiftStamps.query.filter_by(user_id=shiftstamp.user_id, start_time=shiftstamp.start_time).first()
        if comparedShift:
            flash("This Shift Already Exists.", category='error')
        else:
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
