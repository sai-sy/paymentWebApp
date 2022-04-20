# PYTHON DEFAULT
import os

# HELPER FUNCTIONS
from .helper_functions import db_filters as dbf
from .helper_functions.uniqueHex import uniqueCampaignHex
from .shift_route import shift_add_func

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
from .models.campaigns import Campaign_Contracts, CreateCampaignForm, CampaignContractForm, Campaigns, admins, JoinCampaignForm, GovLevels
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
                hex_code = dbf.uniqueCampaignHex(Campaigns)
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
                'litdrop_rate': campaign.pay_rates['litdrop_rate'],
                'commute_rate': campaign.pay_rates['commute_rate']
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
    
    if request.method=='GET':
        if current_user.system_level_id < 3 or current_user.id != campaign_to_update.owner_id:
            return render_template('no_access.html')
        form.gov_level.default = campaign_to_update.gov_level_id
        form.process()

    if request.method=='POST':
        if form.validate_on_submit():
            campaign_to_update.candidate = form.candidate.data
            campaign_to_update.alias = form.alias.data
            campaign_to_update.riding = form.riding.data
            campaign_to_update.year = form.year.data
            campaign_to_update.gov_level_id = form.gov_level.data
            try:
                db.session.commit()
                flash('Campaign Updated Successfully', category='success')
                return render_template('/campaign/campaign_update.html', form=form, campaign_to_update=campaign_to_update)
            except:
                flash('Error: Looks like there was a problem. Try Again Later', category='error')
                return render_template('/campaign/campaign_update.html', form=form, campaign_to_update=campaign_to_update)
        current_app.logger.info(form.errors)

    return render_template('/campaign/campaign_update.html', form=form, campaign_to_update=campaign_to_update)

@campaign_route.route('/campaign/list')
@login_required
def campaign_list():
    if current_user.system_level_id < 3:
        abort(403)
    elif current_user.system_level_id < 8:
        campaigns_grabbed = dbf.all_campaigns_user_admins_list(current_user)
        return render_template('/campaign/campaign_list.html', campaigns=campaigns_grabbed)
    else:
        campaigns_grabbed = Campaigns.query.order_by(Campaigns.date_added)
        return render_template('/campaign/campaign_list.html', campaigns=campaigns_grabbed)    

@campaign_route.route('/campaign/delete/<int:id>')
@login_required
def campaign_delete(id):
    #update so that only owner can access this route
    abort(404)
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
        campaign: Campaigns = Campaigns.query.filter_by(hex_code=form.hex_code.data).first()
        current_app.logger.info(campaign)
        if campaign:
            #Create Contract Here
            new_contract = Campaign_Contracts(
                user_id=current_user.id,
                campaign_id=campaign.id,
                pay_rates=campaign.pay_rates,
                commute_pay=campaign.default_commute_pay
            )
            db.session.add(new_contract)
            db.session.commit()
            flash('You have successfuly joined this campaign!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('No campaign with that code was found', category='error')
    
    return render_template('/campaign/campaign_join.html', form=form)

@campaign_route.route('campaign/dashboard/<int:id>/shift_add', methods=['GET', 'POST'])
@login_required
def campaign_shift_add(id):
    form = ShiftStampForm()
    admin = []
    for c in current_user.admin_campaigns:
        admin.append(c.id)
    if current_user.system_level_id < 3 or id not in admin:
        return render_template('no_access.html')
    elif current_user.system_level_id < 5:
        form.user.choices = dbf.users_in_campaign(id)
        form.campaign.choices = [(str(c.id), str(c.alias)) for c in Campaigns.query.filter(Campaigns.id==id).order_by(desc(Campaigns.alias))]
        form.activity.choices = [str(a.activity) for a in Activities.query.order_by()]
        if form.validate_on_submit():
            shift_add_func(form)
            return redirect(url_for('campaign_route.campaign_shift_add', id=id))
    elif current_user.system_level_id < 8:
        form.campaign.choices = [(str(c.id), str(c.alias))  for c in Campaigns.query.order_by(desc(Campaigns.alias))]
        form.user.choices = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
        if form.validate_on_submit():
            shift_add_func(form)
            return redirect(url_for('shift_route.shift_add', id=id))

    return render_template('/shift/shift_add.html', form=form)

@campaign_route.route('campaign/dashboard/<int:id>/shifts', methods=['GET', 'POST'])
@login_required
def campaign_shift_list(id):
    admin = []
    for c in current_user.admin_campaigns:
        admin.append(c.id)
    if current_user.system_level_id < 3 or id not in admin:
        return render_template('no_access.html')
    else:
        campaigns = [id]
        shifts = ShiftStamps.query.filter(ShiftStamps.campaign_id.in_(campaigns)).order_by(desc(ShiftStamps.start_time))
        return render_template('/shift/shift_list.html', shifts=shifts)

@campaign_route.route('campaign/dashboard/<int:id>/user_list', methods=['GET', 'POST'])
def campaign_user_list(id):
    admin = []
    for c in current_user.admin_campaigns:
        admin.append(c.id)
    if current_user.system_level_id < 3 or id not in admin:
        return render_template('no_access.html')
    else:
        campaign = Campaigns.query.filter(Campaigns.id==id).first()
        if current_user.id == campaign.owner_id:
            status = 'owner'
        else:
            status = 'admin'
        admins = dbf.admins_id_in_campaign(id)
        contracts = Campaign_Contracts.query.filter(Campaign_Contracts.campaign_id==id)
        return render_template('/campaign/campaign_user_list.html', contracts=contracts, admins=admins, status=status, campaign_id=id)

@campaign_route.route('campaign/dashboard/<int:campaign_id>/edit_contract/<int:user_id>', methods=['GET', 'POST'])
def campaign_edit_user_contract(campaign_id, user_id):
    if current_user.system_level_id < 3:
        return render_template('no_access.html')
    else:
        form = CampaignContractForm()
        form.user.choices = [(u.first_name + ' ' + u.last_name) for u in Users.query.filter(Users.id==user_id)]
        form.campaign.choices = [c.alias for c in Campaigns.query.filter(Campaigns.id==campaign_id)]
        contract_to_update = Campaign_Contracts.query.filter(db.and_(Campaign_Contracts.campaign_id==campaign_id, Campaign_Contracts.user_id==user_id)).first()
        form.getting_paid.default = contract_to_update.getting_paid
        form.getting_commute_pay.default = contract_to_update.getting_commute_pay
        form.process()
        if form.validate_on_submit():
            new_pay_rates = {
                'admin_rate': form.admin_rate.data,
                'canvass_rate': form.canvass_rate.data,
                'calling_rate': form.calling_rate.data,
                'general_rate': form.general_rate.data,
                'litdrop_rate': form.litdrop_rate.data,
                'commute_rate': form.commute_rate.data
            }
            pay_rates = {**contract_to_update.pay_rates, **new_pay_rates}

            #contract_to_update.user = form.user.data
            #contract_to_update.campaign = form.campaign.data
            contract_to_update.getting_paid = form.getting_paid.data
            contract_to_update.getting_commute_pay = form.getting_commute_pay.data
            contract_to_update.getting_paid = form.getting_paid.data
            contract_to_update.getting_commute_pay = form.getting_commute_pay.data
            contract_to_update.pay_rates = pay_rates

            try:
                db.session.commit()
                flash('User Contract Updated Successfully', category='success')
                return redirect(url_for('campaign_route.campaign_user_list', id=campaign_id))
            
            except:
                flash('Error: Looks like there was a problem. Try Again Later', category='error')
                return render_template('user/user_update_contract.html', form=form, contract=contract_to_update)
        
        return render_template('user/user_update_contract.html', form=form, contract=contract_to_update)

@campaign_route.route('campaign/dashboard/<int:campaign_id>/add_admin/<int:user_id>')
def campaign_admin_add(campaign_id, user_id):
    current_admins = dbf.campaigns_user_administrating(current_user.id)
    campaigns = dbf.campaigns_user_administrating(user_id)
    if current_user.system_level_id < 3 or campaign_id not in current_admins:
        return render_template('no_access.html')
    else:
        campaign = Campaigns.query.filter(Campaigns.id==campaign_id).first()
        if user_id == campaign.owner_id:
            flash("Cannot remove owner as administrator!", category='error')
            return redirect(url_for('campaign_route.campaign_user_list', id=campaign_id))
        elif campaign_id in campaigns: #if current campaign is in user's admin campaigns
            flash("User is already an administrator.", category='error')
            return redirect(url_for('campaign_route.campaign_user_list', id=campaign_id))
        elif campaign_id not in campaigns:
            try:
                # Add to Admins Table
                db.session.execute(admins.insert().values(user_id=user_id, campaign_id = campaign_id))
                db.session.commit()

                #Increase System Levels
                admin = Users.query.get_or_404(user_id)
                admin.system_level_id = 4
                db.session.commit()
                flash("User promoted to administrator.", category='success')
            except:
                flash("Failed to promote user to administrator.", category='error')
    return redirect(url_for('campaign_route.campaign_user_list', id=campaign_id))

@campaign_route.route('campaign/dashboard/<int:campaign_id>/remove_admin/<int:admin_id>')
def campaign_admin_remove(campaign_id, admin_id):
    abort(404)

@campaign_route.route('campaign/dashboard/<int:id>/payment_list', methods=['GET', 'POST'])
def campaign_payment_list(id):
    admin = []
    for c in current_user.admin_campaigns:
        admin.append(c.id)
    if current_user.system_level_id < 3 or id not in admin:
        return render_template('no_access.html')
    else:
        paystamps = PayStamps.query.filter(PayStamps.campaign_id==id).order_by(desc(PayStamps.payment_date))
        return render_template('/shift/payment_list.html', paystamps=paystamps)

@campaign_route.route('campaign/dashboard/<int:id>/abstract_list', methods=['GET', 'POST'])
def campaign_abstract_list(id):
    admin = []
    for c in current_user.admin_campaigns:
        admin.append(c.id)
    if current_user.system_level_id < 3 or id not in admin:
        return render_template('no_access.html')
    else:
        abstracts = AbstractStamps.query.filter(AbstractStamps.campaign_id==id).order_by(desc(AbstractStamps.date_added))
        return render_template('/shift/abstract_list.html', abstracts=abstracts)

@campaign_route.route('campaign/dashboard/<int:id>/receipt_list', methods=['GET', 'POST'])
def campaign_receipt_list(id):
    admin = []
    for c in current_user.admin_campaigns:
        admin.append(c.id)
    if current_user.system_level_id < 3 or id not in admin:
        return render_template('no_access.html')
    else:
        receipts = Receipts.query.filter(Receipts.campaign_id==id).order_by(desc(Receipts.date))
        return render_template('/shift/receipt_list.html', receipts=receipts)

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
            return render_template('/campaign/campaign_dashboard.html', campaign=campaign_contract.campaign, id=id, status="base")
    
    abort(403)

