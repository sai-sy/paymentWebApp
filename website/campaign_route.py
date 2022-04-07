# PYTHON DEFAULT
import os

# HELPER FUNCTIONS
from .helper_functions.narrow_campaigns import all_campaigns_user_admins_list, users_in_campaign_under_user
from .helper_functions.uniqueHex import uniqueCampaignHex

# FLASK
from flask import Blueprint, jsonify, redirect, render_template, current_app, request, flash, jsonify, Flask, url_for, abort
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy import alias, insert, desc
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

# SQLALCHEMY MODELS
from . import db
from .models.abstracts import AbstractForm, AbstractStamps
from .models.paystamps import PayStamps, PayStampForm
from .models.campaigns import CampaignForm, Campaigns, admins, users_under_campaign, JoinCampaignForm
from .models.users import Users
from .models.people import People
from .models.shiftstamps import ShiftStampForm, ShiftStamps, Activities
from .models.receipts import ReceiptForm, Receipts
from datetime import datetime


campaign_route = Blueprint('campaign_route', __name__)

@campaign_route.route('/campaign/add', methods=['GET', 'POST'])
@login_required
def campaign_create():
    form = CampaignForm()
    form.admins.choices = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
    form.candidate.choices = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
    if form.validate_on_submit():
        current_app.logger.info('1')
        alias_check = form.alias.data
        print('looking')
        campaign = Campaigns.query.filter_by(alias=alias_check).first()
        if campaign:
            flash("Campaign Alias Already Exists. Must be Unique", category='error')
        else:
            print('attemping add')
            campaign = Campaigns(
                #candidate_id = form.candidate.data,
                candidate = form.candidate.data,
                alias = form.alias.data,
                riding = form.riding.data,
                year = form.year.data,
                gov_level = form.gov_level.data,
                owner_id = current_user.id,
                hex_code = uniqueCampaignHex(Campaigns),
                hourly_rate = form.hourly_rate.data
            )
            db.session.add(campaign)
            db.session.commit()

            # Update Owner to Admin
            current_user_id = current_user.id
            owner = Users.query.get_or_404(current_user_id)
            owner.system_level_id = 4

            # Add to Admin Table and User Under Campaign Table
            campaign = Campaigns.query.filter_by(alias=alias_check).first()

            for dataItem in form.admins.data:
                admin = Users.query.get_or_404(dataItem)
                admin.system_level_id = 4
                db.session.commit()
                db.session.execute(admins.insert().values(user_id=dataItem, campaign_id=campaign.id))
                db.session.execute(users_under_campaign.insert().values(user_id=dataItem, campaign_id=campaign.id))

            db.session.execute(admins.insert().values(user_id=current_user.id, campaign_id = campaign.id))
            db.session.execute(users_under_campaign.insert().values(user_id=current_user.id, campaign_id = campaign.id))

            db.session.commit()

            #Empty Form
            form.candidate.data = ''
            form.alias.data = ''
            form.alias.data = ''
            form.year.data = ''
            form.gov_level.data = ''
            form.admins.data = ''
            flash("Campaign Added Successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template('/campaign/campaign_create.html', form=form)

@campaign_route.route("/campaign/update/<int:id>", methods=['GET', 'POST'])
@login_required
def campaign_update(id):
    form = CampaignForm()
    campaign_to_update = Campaigns.query.get_or_404(id)
    choiceMath = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
    form.admins.choices = choiceMath
    if form.validate_on_submit():
        campaign_to_update.candidate = request.form['candidate']
        campaign_to_update.alias = request.form['alias']
        campaign_to_update.riding = request.form['riding']
        campaign_to_update.year = request.form['year']
        campaign_to_update.gov_level = request.form['gov_level']
        try:
            db.session.commit()
            flash('Campaign Updated Successfully', category='success')
            return render_template('home.html', form=form, name_to_update=campaign_to_update)
        except:
            flash('Error: Looks like there was a problem. Try Again Later', category='error')
            form.candidate.data = ''
            form.alias.data = ''
            form.alias.data = ''
            form.year.data = ''
            form.gov_level.data = ''
            form.admins.data = ''
            return render_template('/campaign/campaign_update.html', form=form, campaign_to_update=campaign_to_update)
    return render_template('/campaign/campaign_update.html', form=form, campaign_to_update=campaign_to_update)

@campaign_route.route('/campaign/list')
@login_required
def campaign_list():
    if current_user.system_level_id < 3:
        abort(403)
    elif current_user.system_level_id < 8:
        campaigns_grabbed = all_campaigns_user_admins_list(current_user)
        return render_template('/campaign/campaign_list.html', campaigns=campaigns_grabbed)
    else:
        campaigns_grabbed = Campaigns.query.order_by(Campaigns.date_added)
        return render_template('/campaign/campaign_list.html', campaigns=campaigns_grabbed)
    

@campaign_route.route('/campaign/delete/<int:id>')
@login_required
def campaign_delete(id):
    campaign_to_delete = Campaigns.query.get_or_404(id)
    try:
        db.session.delete(campaign_to_delete)
        db.session.commit()
        flash("Campaign Deleted Successfully", category='success')
        return redirect(url_for('views.home'))
    except:
        flash("Campaign Was Not Deleted Successfully", category='error')
        return redirect(url_for('campaign_route.campaign_list'))


@campaign_route.route('/campaign/join', methods=['GET', 'POST'])
@login_required
def campaign_join():
    form = JoinCampaignForm()
    if form.validate_on_submit():
        campaign = Campaigns.query.filter_by(hex_code=form.hex_code.data).first()
        current_app.logger.info(campaign)
        if campaign:
            db.session.execute(users_under_campaign.insert().values(user_id=current_user.id, campaign_id=campaign.id))
            db.session.commit()
            flash('You have successfuly joined this campaign!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('No campaign with that code was found', category='error')
    
    return render_template('/campaign/campaign_join.html', form=form)

@campaign_route.route('campaign/dashboard/<int:id>/shifts', methods=['GET', 'POST'])
@login_required
def campaign_shift_list(id):
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    else:
        campaigns = [id]
        shifts = ShiftStamps.query.filter(ShiftStamps.campaign_id.in_(campaigns)).order_by(desc(ShiftStamps.start_time))
        current_app.logger.info(shifts)
        return render_template('/shift/shift_list.html', shifts=shifts)


@campaign_route.route("/campaign/dashboard/<int:id>", methods=['GET', 'POST'])
@login_required
def campaign_dashboard(id):
    campaign = Campaigns.query.get_or_404(id)
    return render_template('/campaign/campaign_dashboard.html', campaign=campaign)
