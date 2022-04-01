from secrets import choice
from flask import Blueprint, jsonify, redirect, render_template, request, flash, jsonify, Flask, url_for
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy import insert
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from . import db
from .models.users import Users
from .models.people import People
from .models.campaigns import CampaignForm, Campaigns, admins
campaign_route = Blueprint('campaign_route', __name__)

@campaign_route.route('/campaign_add', methods=['GET', 'POST'])
@login_required
def campaign_add():
    form = CampaignForm()
    choiceMath = [(str(u.id), str(u.first_name + ' ' + u.last_name)) for u in Users.query.order_by('first_name')]
    form.admins.choices = choiceMath
    form.candidate.choices = choiceMath
    if form.validate_on_submit():
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
            )
            db.session.add(campaign)
            db.session.commit()

            # Update Owner
            owner = Users.get_or_404(current_user.id)
            owner.system_level_id = 4
            # Create Admin Table
            campaign = Campaigns.query.filter_by(alias=alias_check).first()
            #campaign.admins.append(form.admins.data)
            for dataItem in form.admins.data:
                db.session.execute(admins.insert().values(user_id=dataItem, campaign_id=campaign.id))
                db.session.commit()

            db.session.execute(admins.insert().values(user_id=current_user.id, campaign_id = campaign.id))

            #Empty DataBase
            form.candidate.data = ''
            form.alias.data = ''
            form.alias.data = ''
            form.year.data = ''
            form.gov_level.data = ''
            form.admins.data = ''
            flash("Campaign Added Successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template('/campaign/campaign_add.html', form=form)

@campaign_route.route("/campaign_update/<int:id>", methods=['GET', 'POST'])
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


@campaign_route.route('/campaign_list')
@login_required
def campaign_list():
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