# PYTHON DEFAULT
import os, csv
from io import StringIO

# HELPER FUNCTIONS
from .helper_functions.narrow_campaigns import all_campaigns_user_admins_list, all_campaigns_user_in, all_campaigns_user_admins, users_in_campaign_user_adminning

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
from datetime import datetime

export_route = Blueprint('export_route', __name__)

@export_route.route("/export_data", methods=['GET', 'POST'])
@login_required
def export_data():
    shiftstamps = ShiftStamps.query.order_by(desc(ShiftStamps.start_time))
    response = export_data_func(shiftstamps)
    return response

def export_data_func(shiftstamps):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows([(shift.user_id, shift.start_time, shift.end_time, shift.minutes, shift.campaign_id, shift.activity_id) for shift in shiftstamps])
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=database.csv'
    response.headers["Content-type"] = "text/csv"
    return response