# PYTHON DEFAULT
import imp
import os

# HELPER FUNCTIONS
from .helper_functions.narrow_campaigns import all_campaigns_user_in, all_campaigns_user_admins, users_in_campaign_user_adminning, all_campaigns
from .helper_functions import load_sheet

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

# OTHER
import pandas as pd
import datetime as dt

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
        campaigns_grabbed = all_campaigns
        import_data_func(form, campaigns_grabbed)

    return render_template('/import/import_data.html', form=form)


def import_data_func(form, wl_campaigns):
    if form.validate_on_submit():
        db_filename = 'import_' + current_user.alias + '_' + str(form.import_type.data).lower() + '_' + str(dt.date.today())
        i = 1
        while(True):        
            searched_file = Imports.query.filter_by(file_name=db_filename).first()
            if searched_file:
                db_filename = db_filename + '_' + str(i) 
                i = i + 1
                continue
            else:
                import_object = Imports(
                    file_name = db_filename,
                    person_imported = current_user.id,
                )
                db.session.add(import_object)
                db.session.commit()
                break

        if form.import_type.data == "Shifts":
            #Save File
            file = form.file.data
            filename = secure_filename(file.filename)
            assets_dir = os.path.join(os.path.dirname(current_app.instance_path), current_app.config['IMPORT_FOLDER'])
            if file.filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                file.save(os.path.join(assets_dir, db_filename+file_ext))
            
            #Process File
            load_sheet.prod_start(db_filename+file_ext, form.import_type.data)

        else:
            flash('This import function hasnt been created yet.', category='error')

