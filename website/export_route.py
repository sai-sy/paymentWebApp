# PYTHON DEFAULT
import os, csv
from io import StringIO

# HELPER FUNCTIONS
from .helper_functions.db_filters import all_campaigns_user_in, all_campaigns_user_admins, users_in_campaign_user_adminning, all_campaigns

# FLASK
from flask import Blueprint, send_file, jsonify, redirect, render_template, current_app, request, flash, jsonify, Flask, url_for, abort, make_response
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
from .models.campaigns import Campaigns
from .models.users import Users
from .models.people import People
from .models.shiftstamps import ShiftStampForm, ShiftStamps, Activities
from .models.receipts import ReceiptForm, Receipts
from .models.imports import ImportForm, Imports
from .models.exports import ExportForm
from datetime import datetime

export_route = Blueprint('export_route', __name__)

@export_route.route("/export_data", methods=['GET', 'POST'])
@login_required
def export_data():

    if current_user.system_level_id < 3:
        abort(403)
    elif current_user.system_level_id < 8:
        campaigns_grabbed = all_campaigns_user_admins(current_user)
    else:
        campaigns_grabbed = all_campaigns

    form = ExportForm()
    form.campaign.choices = campaigns_grabbed

    if form.validate_on_submit():
        response = export_data_func(form)
        return response
        #return redirect(url_for('export_route.export_data'))
    return render_template('/export/export_data.html', form=form)

def export_data_func(form: ExportForm):
    if form.export_type.data == "Shifts":
        #campaign = form.campaign.data
        #shiftstamps = ShiftStamps.query.filter(ShiftStamps.campaign_id.in_(campaign)).order_by(desc(ShiftStamps.start_time))
        shiftstamps = ShiftStamps.query.order_by(desc(ShiftStamps.start_time))
        response = export_shifts_func(shiftstamps)
        return response

def export_shifts_func(shiftstamps):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows([(shift.user, shift.start_time, shift.end_time, shift.minutes, shift.campaign.alias, shift.activity_id) for shift in shiftstamps])
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=database.csv'
    response.headers["Content-type"] = "text/csv"
    return response