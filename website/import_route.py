# PYTHON DEFAULT
import os

# HELPER FUNCTIONS
from .helper_functions.narrow_campaigns import all_campaigns_user_in, all_campaigns_user_admins, users_in_campaign_under_user

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
from .models.campaigns import Campaigns
from .models.users import Users
from .models.people import People
from .models.shiftstamps import ShiftStampForm, ShiftStamps, Activities
from .models.receipts import ReceiptForm, Receipts
from .models.imports import ImportForm, Imports
from datetime import datetime

import_route = Blueprint('import_route', __name__)

@import_route.route("/import_data", methods=['GET', 'POST'])
@login_required
def import_data():
    form = ImportForm()
    if current_user.system_level_id < 3:
        abort(403)
    elif current_user.system_level_id < 8:
        campaigns_grabbed = all_campaigns_user_admins(current_user)
        import_data_func(form, campaigns_grabbed)
    else:
        campaigns_grabbed = Campaigns.query.order_by(Campaigns.date_added)
        import_data_func(form, campaigns_grabbed)

    return render_template('/import/import_data.html', form=form)


def import_data_func(form, wl_campaigns):
    pass

