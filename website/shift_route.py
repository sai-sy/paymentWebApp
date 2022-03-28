from calendar import c
from secrets import choice
from flask import Blueprint, jsonify, redirect, render_template, current_app, request, flash, jsonify, Flask, url_for, abort
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy import alias, insert, desc
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from .models.paystamps import PayStamps, PayStampForm
from .models.campaigns import Campaigns
from . import db
from .models.users import Users
from .models.people import People
from .models.shiftstamps import ShiftStampForm, ShiftStamps, Activities
from .models.receipts import ReceiptForm, Receipts
from datetime import datetime
import os
shift_route = Blueprint('shift_route', __name__)

def shift_add_func(form: ShiftStampForm):
    form.activity.choices = [str(a.activity) for a in Activities.query.order_by()]
    form.campaign.choices = [str(c.alias) for c in Campaigns.query.order_by()]
    if form.validate_on_submit():

        calcedStart = datetime.combine(form.date.data, datetime.strptime(form.start_time.data, '%H:%M:%S').time())
        comparedShift = ShiftStamps.query.filter_by(user_id=form.user.data, start_time=calcedStart, campaign_id=form.campaign.data).first()
        if comparedShift:
            flash("This Shift Already Exists.", category='error')
        else:
            founduser = Users.query.filter_by(id=form.user.data).first()
            foundactivity = Activities.query.filter_by(activity=form.activity.data).first()
            shiftstamp = ShiftStamps(user_id=founduser.id, user=founduser, start_time=calcedStart,
                end_time=datetime.combine(form.date.data, datetime.strptime(form.end_time.data, '%H:%M:%S').time()),
                activity_id=form.activity.data,
                activity=foundactivity
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

@shift_route.route('/shift_add', methods=['GET', 'POST'])
@login_required
def shift_add():
    form = ShiftStampForm()
    choiceMath = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by()]
    form.user.choices = choiceMath
    form.activity.choices = [str(a.activity) for a in Activities.query.order_by()]
    form.campaign.choices = [(str(c.id), str(c.alias))  for c in Campaigns.query.order_by()]
    if form.validate_on_submit():

        calcedStart = datetime.combine(form.date.data, datetime.strptime(form.start_time.data, '%H:%M:%S').time())
        comparedShift = ShiftStamps.query.filter_by(user_id=form.user.data, start_time=calcedStart).first()
        if comparedShift:
            flash("This Shift Already Exists.", category='error')
        else:
            founduser = Users.query.filter_by(id=form.user.data).first()
            foundactivity = Activities.query.filter_by(activity=form.activity.data).first()
            shiftstamp = ShiftStamps(user_id=founduser.id, user=founduser, start_time=calcedStart,
                end_time=datetime.combine(form.date.data, datetime.strptime(form.end_time.data, '%H:%M:%S').time()),
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

@shift_route.route('/shift_list', methods=['GET', 'POST'])
@login_required
def shift_list():
    if current_user.system_level_id < 3:
        
        return render_template('no_access.html')
    elif current_user.system_level_id < 5:
        campaigns = [c.id for c in current_user.admin_campaigns]
        current_app.logger.info(campaigns)
        shifts = ShiftStamps.query.filter(ShiftStamps.campaign_id.in_(campaigns)).order_by(desc(ShiftStamps.start_time))
        current_app.logger.info(shifts)
        return render_template('/shift/shift_list.html', shifts=shifts)
    else:
        current_app.logger
        shifts = ShiftStamps.query.filter_by().order_by(desc(ShiftStamps.start_time))
        return render_template('/shift/shift_list.html', shifts=shifts)

@shift_route.route('/shift/delete/<int:id>')
@login_required
def shift_delete(id):
    shift_to_delete = ShiftStamps.query.get_or_404(id)
    try:
        db.session.delete(shift_to_delete)
        db.session.commit()
        flash("Shift Deleted Successfully", category='success')
        return redirect(url_for('shift_route.shift_list'))
    except:
        flash("Shift Was Not Deleted Successfully", category='error')
        return redirect(url_for('shift_route.shift_list'))

# RECEIPTS

@shift_route.route('/receipt_upload', methods=['GET', 'POST'])
@login_required
def receipt_upload():
    form = ReceiptForm()
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    elif current_user.system_level_id < 5:
        uploaded_file = form.image.data
        current_app.logger.info('enter ten')
        campaigns = [(c.id, str(c.alias)) for c in current_user.admin_campaigns]
        form.campaigns.choices = campaigns
        choiceMath = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
        form.users.choices = choiceMath
        if form.validate_on_submit():
            receipt_upload_func(form)
        else:
            current_app.logger.info('notvalidated')
            current_app.logger.info(form.errors)
        return render_template('/shift/receipt_upload.html', form=form)
    else:
        uploaded_file = form.image.data
        current_app.logger.info('enter ten')
        campaigns = [(c.id, str(c.alias)) for c in Campaigns.query.filter_by()]
        form.campaigns.choices = campaigns
        choiceMath = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
        form.users.choices = choiceMath
        if form.validate_on_submit():
            receipt_upload_func(form)
        else:
            current_app.logger.info('notvalidated')
            current_app.logger.info(form.errors)
        return render_template('/shift/receipt_upload.html', form=form)


def receipt_upload_func(form: ReceiptForm):
    user = Users.query.filter_by(id=form.users.data).first()
    campaign = Campaigns.query.filter_by(id=form.campaigns.data).first()
    db_filename = campaign.alias + '_' + user.first_name + '_' + user.last_name + '_' + '_'+ str(form.date.data)
    while(True):
        i = 1
        searched_file = Receipts.query.filter_by(image_name=db_filename).first()
        if searched_file:
            db_filename = db_filename + '_' + str(i) 
            i = i + 1
        else:
            receipt = Receipts(
                user_id = form.users.data,
                date = form.date.data,
                image_name = db_filename,
                amount = form.amount.data,
                campaign_id = form.campaigns.data
            )
            db.session.add(receipt)
            db.session.commit()
            break
    assets_dir = os.path.join(os.path.dirname(current_app.instance_path), 'assets', 'receipts')
    current_app.logger.info('validated')
    uploaded_file = form.image.data
    filename = secure_filename(uploaded_file.filename)
    if uploaded_file.filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(assets_dir, db_filename+file_ext))
        flash("File Saved Successfully", category='success')
    return redirect(url_for('views.home'))


@shift_route.route('/receipt_list', methods=['GET', 'POST'])
@login_required
def receipt_list():
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    elif current_user.system_level_id < 5:
        campaigns = [c.id for c in current_user.admin_campaigns]
        current_app.logger.info(campaigns)
        receipts = Receipts.query.filter(Receipts.campaign_id.in_(campaigns)).order_by(desc(Receipts.date))
        return render_template('/shift/receipt_list.html', receipts=receipts)
    else:
        receipts = Receipts.query.filter_by().order_by(desc(Receipts.date))
        return render_template('/shift/receipt_list.html', receipts=receipts)

@shift_route.route('/receipt/delete/<int:id>')
@login_required
def receipt_delete(id):
    receipt_to_delete = Receipts.query.get_or_404(id)
    try:
        db.session.delete(receipt_to_delete)
        db.session.commit()
        flash("Receipt Deleted Successfully", category='success')
        return redirect(url_for('shift_route.receipt_list'))
    except:
        flash("Receipt Was Not Deleted Successfully", category='error')
        return redirect(url_for('shift_route.receipt_list'))

# PAYMENTS
@shift_route.route('/paystamp_upload', methods=['GET', 'POST'])
@login_required
def paystamp_upload():
    form = PayStampForm()
    form.activity.choices = [str(a.activity) for a in Activities.query.order_by()]
    users = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    elif current_user.system_level_id < 5:
        campaigns = [(c.id, str(c.alias)) for c in current_user.admin_campaigns]
        form.campaign.choices = campaigns   
        form.user.choices = users
        if form.validate_on_submit():
            paystamp_upload_func(form)
        else:
            current_app.logger.info('notvalidated')
            current_app.logger.info(form.errors)
        return render_template('/shift/payment_upload.html', form=form)
    else:
        campaigns = [(c.id, str(c.alias)) for c in Campaigns.query.filter_by()]
        form.campaign.choices = campaigns
        form.user.choices = users
        if form.validate_on_submit():
            paystamp_upload_func(form)
        else:
            current_app.logger.info('notvalidated')
            current_app.logger.info(form.errors)
        return render_template('/shift/payment_upload.html', form=form)


def paystamp_upload_func(form: PayStampForm):
    # Load variables
    user = Users.query.filter_by(id=form.user.data).first()
    campaign = Campaigns.query.filter_by(id=form.campaign.data).first()
    searched_paystamp = PayStamps.query.filter_by(user_id=form.user.data, payment_date=form.date.data, campaign_id=form.campaign.data).first()

    # Search for this paystamp, if non-existent, add to database
    if searched_paystamp:
        flash("This Payment Record Already Exists.", category='error')
    else:
        paystamp = PayStamps(
            user_id = form.user.data,
            payment_date = form.date.data,
            amount = form.amount.data,
            campaign_id = form.campaign.data,
            activity_id = form.activity.data,
            notes = form.notes.data,
        )
        db.session.add(paystamp)
        db.session.commit()

        form.user.data = ''
        form.date.data = ''
        form.amount.data = ''
        form.campaign.data = ''
        form.activity.data = ''
        form.notes.data = ''

        flash("Payment Record Saved Successfully", category='success')
        return redirect(url_for('views.home'))

@shift_route.route("/paystamp_list", methods=['GET', 'POST'])
@login_required
def payment_list():
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    elif current_user.system_level_id < 5:
        campaigns = [c.id for c in current_user.admin_campaigns]
        current_app.logger.info(campaigns)
        paystamps = PayStamps.query.filter(PayStamps.cam.in_(campaigns)).order_by(desc(PayStamps.payment_date))
        return render_template('/shift/payment_list.html', paystamps=paystamps)
    else:
        paystamps = PayStamps.query.filter_by().order_by(desc(PayStamps.payment_date))
        return render_template('/shift/payment_list.html', paystamps=paystamps)

@shift_route.route('/payment/delete/<int:id>')
@login_required
def paystamp_delete(id):
    paystamp_to_delete = PayStamps.query.get_or_404(id)
    try:
        db.session.delete(paystamp_to_delete)
        db.session.commit()
        flash("Payment Record Deleted Successfully", category='success')
        return redirect(url_for('shift_route.payment_list'))
    except:
        flash("Payment Record Was Not Deleted Successfully", category='error')
        return redirect(url_for('shift_route.payment_list'))