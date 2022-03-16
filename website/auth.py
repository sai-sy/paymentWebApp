from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from werkzeug.security import generate_password_hash, check_password_hash

from paymentWebApp.website.models.user import Users
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired


#Models
from .models.person import People, LoginForm, SignUpForm
from .models.user import Users 

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    name = None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        return redirect(url_for('views.home'))
    return render_template('login.html', name=name, form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    first_name = None
    form = SignUpForm()
    if request.method=='POST':
        email_check = form.email.data
        user = Users.query.filter_by(email=email_check).first()
        if user:
            flash("Email Already Exists", category='error')
        elif request.form['password1'].isspace() or request.form['password2'].isspace():
            flash('Password must not be empty')
        elif request.form['password1'] != request.form['password2']:
            flash('Passwords don\'t match', category='error')
        else:
            user = Users(first_name=form.first_name.data, last_name=form.last_name.data,email=form.email.data, phone=form.phone.data, password=form.password1.data)
            db.session.add(user)
            db.session.commit()
            first_name = form.first_name.data
            form.first_name.data = ''
            form.last_name.data = ''
            form.phone.data = ''
            form.password1.data = ''
            form.password2.data = ''
            form.email.data = ''
            flash("User Added Successfully!")
            return redirect(url_for('views.home'))
    return render_template('signup.html', form=form, name=first_name)

@auth.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    form = SignUpForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method=='POST':
        if request.form['password1'].isspace() or request.form['password2'].isspace():
            flash('Password must not be empty')
        elif request.form['password1'] != request.form['password2']:
            flash('Passwords don\'t match', category='error')
        else:
            name_to_update.first_name = request.form['first_name']
            name_to_update.last_name = request.form['last_name']
            name_to_update.email = request.form['email']
            name_to_update.phone = request.form['phone']
            name_to_update.password = request.form['password1']
            try:
                db.session.commit()
                flash('User Updated Successfully', category='success')
                return render_template('home.html', form=form, name_to_update=name_to_update)
            except:
                flash('Error: Looks like there was a problem. Try Again Later', category='error')
                return render_template('update.html', form=form, name_to_update=name_to_update)
    return render_template('update.html', form=form, name_to_update=name_to_update)