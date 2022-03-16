from flask import Flask, appcontext_popped, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys
import os
sys.path.insert(1, 'C:\saiscripts\intercept_branch\Payment Web App Project')
from paymentWebApp import imbedded as i

db = SQLAlchemy()
DB_NAME = "main"

def create_app():
    #Flask Instance
    app = Flask(__name__)

    #Database
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    mysqlString = 'mysql+pymysql://'+i.s.usr+':'+i.s.psswd+'@'+i.s.hst+'/'+DB_NAME
    #+print(mysqlString)
    app.config['SQLALCHEMY_DATABASE_URI'] = mysqlString
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .models.user import Users
    from .models.person import People

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    

    return app


def handle_session_add_error(addContent, db):
    pass 