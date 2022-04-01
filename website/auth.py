from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
#Internal
from . import db
#Flask WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired
#Models
from .models.people import People
from .models.users import Users, LoginForm, SignUpForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                form.email.data = ''
                form.password.data = ''
                next = request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                return redirect(url_for('views.home'))
            else:
                form.email.data = ''
                form.password.data = ''
                flash('Incorrect password, ty again.', category='error')
        else:
            form.email.data = ''
            form.password.data = ''
            flash('Email does not exist', category='error')

        form.email.data = ''
        form.password.data = ''
    return render_template('/user/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    first_name = None
    form = SignUpForm()
    if form.validate_on_submit():
        email_check = form.email.data
        user = Users.query.filter_by(email=email_check).first()
        if user:
            flash("Email Already Exists", category='error')
        else:
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password1.data, "sha256")
            user = Users(
            first_name=form.first_name.data, 
            last_name=form.last_name.data,
            email=form.email.data, 
            phone=form.phone.data, 
            password_hash=hashed_pw,            
            )

            db.session.add(user)
            db.session.commit()

            first_name = form.first_name.data
            form.first_name.data = ''
            form.last_name.data = ''
            form.phone.data = ''
            form.password1.data = ''
            form.password2.data = ''
            form.email.data = ''
            flash("User Added Successfully!", category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template('/user/signup.html', form=form, name=first_name)

@auth.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def user_update(id):
    theForm = SignUpForm()
    name_to_update = Users.query.get_or_404(id)
    if theForm.validate_on_submit():
        name_to_update.first_name = request.form['first_name']
        name_to_update.last_name = request.form['last_name']
        name_to_update.email = request.form['email']
        name_to_update.phone = request.form['phone']
        name_to_update.password_hash = request.form['password1']
        try:
            db.session.commit()
            flash('User Updated Successfully', category='success')
            return redirect(url_for('views.home'))
        except:
            flash('Error: Looks like there was a problem. Try Again Later', category='error')
            first_name = theForm.first_name.data
            theForm.first_name.data = ''
            theForm.last_name.data = ''
            theForm.phone.data = ''
            theForm.password1.data = ''
            theForm.password2.data = ''
            theForm.email.data = ''
            return render_template('/user/user_update.html', form=theForm, name_to_update=name_to_update)
    return render_template('/user/user_update.html', form=theForm, name_to_update=name_to_update)

@auth.route('/user_list/delete/<int:id>')
@login_required
def user_delete(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully", category='success')
        return redirect(url_for('views.home'))
    except:
        flash("User Was Not Deleted Successfully", category='error')
        return redirect(url_for('views.user_list'))