# PYTHON DEFAULT
import os

# HELPER FUNCTIONS
from .helper_functions.db_filters import users_in_campaign, admins_in_campaign, all_campaigns_user_admins_list, users_in_campaign_user_adminning
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
from .models.campaigns import Campaign_Contracts, CreateCampaignForm, Campaigns, admins, JoinCampaignForm, GovLevels
from .models.users import Users
from .models.people import People
from .models.shiftstamps import ShiftStampForm, ShiftStamps, Activities
from .models.receipts import ReceiptForm, Receipts
from datetime import datetime


campaign_route = Blueprint('campaign_route', __name__)

@campaign_route.route('/campaign/add', methods=['GET', 'POST'])
@login_required
def campaign_create():
    form = CreateCampaignForm()
    form.gov_level.choices=[level.level for level in GovLevels.query.filter_by()]
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
                gov_level_id = form.gov_level.data,
                owner_id = current_user.id,
                hex_code = uniqueCampaignHex(Campaigns)
            )
            db.session.add(campaign)
            db.session.commit()

            # Update Owner to Admin System Level
            current_user_id = current_user.id
            owner = Users.query.get_or_404(current_user_id)
            owner.system_level_id = 4

            # Add to Admin Table and User Under Campaign Table
            campaign:Campaigns = Campaigns.query.filter_by(alias=alias_check).first()

            '''
            for dataItem in form.admins.data:
                admin = Users.query.get_or_404(dataItem)
                admin.system_level_id = 4
                db.session.commit()
                db.session.execute(admins.insert().values(user_id=dataItem, campaign_id=campaign.id))
            '''

            db.session.execute(admins.insert().values(user_id=current_user.id, campaign_id = campaign.id))
            #Make Admin Part of Campaign here
            pay_rates = { 
                'admin_rate': campaign.pay_rates['admin_rate'],
                'canvass_rate': campaign.pay_rates['canvass_rate'],
                'calling_rate': campaign.pay_rates['calling_rate'],
                'general_rate': campaign.pay_rates['general_rate'],
                'litdrop_rate': campaign.pay_rates['litdrop_rate']
            }
            owner_contract = Campaign_Contracts(
                user_id =current_user.id,
                campaign_id=campaign.id,
                pay_rates=pay_rates,
            )
            db.session.add(owner_contract)
            db.session.commit()

            #Empty Form
            form.candidate.data = ''
            form.alias.data = ''
            form.alias.data = ''
            form.year.data = ''
            form.gov_level.data = ''
            flash("Campaign Added Successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template('/campaign/campaign_create.html', form=form)

@campaign_route.route("/campaign/update/<int:id>", methods=['GET', 'POST'])
@login_required
def campaign_update(id):
    form = CreateCampaignForm()
    form.gov_level.choices=[level.level for level in GovLevels.query.filter_by()]
    campaign_to_update = Campaigns.query.get_or_404(id)
    if form.validate_on_submit():
        campaign_to_update.candidate = request.form['candidate']
        campaign_to_update.alias = request.form['alias']
        campaign_to_update.riding = request.form['riding']
        campaign_to_update.year = request.form['year']
        campaign_to_update.gov_level_id = request.form['gov_level']
        try:
            db.session.commit()
            flash('Campaign Updated Successfully', category='success')
            return render_template('/campaign/campaign_update.html', form=form, name_to_update=campaign_to_update)
        except:
            flash('Error: Looks like there was a problem. Try Again Later', category='error')
            form.candidate.data = ''
            form.alias.data = ''
            form.alias.data = ''
            form.year.data = ''
            form.gov_level.data = ''
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
            #Create Contract Here
            new_contract = Campaign_Contracts(
                user_id =current_user.id,
                campaign_id=campaign.id,
                admin_rate=campaign.pay_rates['admin_rate'],
                canvass_rate=campaign.pay_rates['canvass_rate'],
                calling_rate=campaign.pay_rates['calling_rate'],
                general_rate=campaign.pay_rates['general_rate'],
                litdrop_rate = campaign.pay_rates['litdrop_rate']
            )
            db.session.add(new_contract)
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

@campaign_route.route('campaign/dashboard/<int:id>/admin_list', methods=['GET', 'POST'])
def campaign_admin_list(id):
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    else:
        admins = admins_in_campaign(id)
        return render_template('/campaign/campaign_admin_list.html', admins=admins, campaign_id=id)

@campaign_route.route('campaign/dashboard/<int:id>/user_list', methods=['GET', 'POST'])
def campaign_user_list(id):
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    else:
        users = users_in_campaign(id)
        return render_template('/campaign/campaign_user_list.html', users=users, campaign_id=id)

@campaign_route.route('campaign/dashboard/<int:campaign_id>/edit_contract/<int:user_id>')
def campaign_edit_user_contract(campaign_id, user_id):
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    else:
        contract = Campaign_Contracts.query.filter(db.and_(Campaign_Contracts.campaign_id==campaign_id, Campaign_Contracts.user_id==user_id)).first()
        return render_template('user/user_update_contract.html', contract=contract)
         

@campaign_route.route('campaign/dashboard/<int:campaign_id>/remove_admin/<int:admin_id>')
def admin_remove(campaign_id, admin_id):
    abort(403)

@campaign_route.route('campaign/dashboard/<int:id>/payment_list', methods=['GET, POST'])
def campaign_payment_list(id):
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    else:
        pass

@campaign_route.route("/campaign/dashboard/<int:id>", methods=['GET', 'POST'])
@login_required
def campaign_dashboard(id):
    for campaign in current_user.campaigns_owned:
        if campaign.id == id:
            return render_template('/campaign/campaign_dashboard.html', campaign=campaign, id=id, status='owner')
    for campaign in current_user.admin_campaigns:
        if campaign.id == id:
            return render_template('/campaign/campaign_dashboard.html', campaign=campaign, id=id, status="admin")
        
    for campaign_contract in current_user.campaign_contracts:
        if campaign_contract.campaign_id == id:
            return render_template('/campaign/campaign_dashboard.html', campaign=campaign, id=id, status="base")
        else:
            abort(403)

